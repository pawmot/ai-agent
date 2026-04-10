import argparse
parser = argparse.ArgumentParser(description="Chatbot")
_ = parser.add_argument("user_prompt", type=str, help="User prompt")
_ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

from dotenv import load_dotenv
_ = load_dotenv()

# import litellm
# print(litellm.supports_parallel_function_calling(model="anthropic/claude-sonnet-4-6"))
# print(litellm.supports_parallel_function_calling(model="anthropic/claude-haiku-4-5"))
# print(litellm.supports_function_calling(model="anthropic/claude-sonnet-4-6"))
# print(litellm.supports_function_calling(model="anthropic/claude-haiku-4-5"))
# exit(0)

from litellm import acompletion, experimental_mcp_client
from prompts import system_prompt
messages = [
    {"role": "system", "content": [{ "type": "text", "text": system_prompt }]},
    {"role": "user", "content": [{ "type": "text", "text": args.user_prompt }]}
]
from fn_decl_litellm import schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
available_tools = [schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
from fn_call_litellm import call_function
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

from contextlib import AsyncExitStack
from dataclasses import dataclass

# TODO: sth is fucked here when the final model response is sent for tracing, investigate
import litellm
litellm.callbacks = ["langsmith"]
litellm.langsmith_batch_size = 1

@dataclass
class McpServerConfig:
    pass

@dataclass
class StdioMcpServerConfig(McpServerConfig):
    command: str
    args: list[str]
    working_dir: str

@dataclass
class HttpMcpServerConfig(McpServerConfig):
    url: str

@dataclass
class McpConnection:
    session: ClientSession
    tools: list



mcp_servers: dict[str, McpServerConfig] = {
    "add": StdioMcpServerConfig(
        command="uv", 
        args=["run", "main.py"],
        working_dir="./mcp_servers/add"
    ),
    "power": HttpMcpServerConfig(
        url="http://localhost:8123/mcp"
    )
}

import subprocess
class McpManager:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.connections: dict[str, McpConnection] = {}

    async def initialize(self):
        for name, config in mcp_servers.items():
            if type(config) is StdioMcpServerConfig:
                print(f"Starting stdio MCP server '{name}'")
                r, w = await self.exit_stack.enter_async_context(stdio_client(StdioServerParameters(command=config.command, args=config.args, cwd=config.working_dir), errlog=subprocess.DEVNULL))
            elif type(config) is HttpMcpServerConfig:
                print(f"Connecting to http MCP server '{name}'")
                r, w, _ = await self.exit_stack.enter_async_context(streamable_http_client(config.url))
            else:
                raise ValueError(f"Unsupported MCP server config type: {type(config)}")


            session = await self.exit_stack.enter_async_context(ClientSession(r, w))
            await session.initialize()
            tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")
            self.connections[name] = McpConnection(session=session, tools=tools)
    
    def get_mcp_tools(self):
        import copy
        all_tools = []
        for mcp_name, connection in self.connections.items():
            for tool in connection.tools:
                t = copy.deepcopy(tool)
                t["function"]["name"] = f"mcp__{mcp_name}__{tool['function']['name']}"
                all_tools.append(t)
        return all_tools

    async def call_mcp_tool(self, tool_call):
        _, mcp_name, tool_name = tool_call.function.name.split("__", 2)
        print(f"- Calling MCP tool {mcp_name}/{tool_name}")
        connection = self.connections.get(mcp_name)
        if not connection:
            raise ValueError(f"No MCP connection found for name: {mcp_name}")
        
        import json
        result = await connection.session.call_tool(tool_name, json.loads(tool_call.function.arguments))
        return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": result.structuredContent
        }

    async def close(self):
        await self.exit_stack.aclose()

from langsmith import traceable
from langsmith.run_trees import RunTree
from langsmith.run_helpers import get_current_run_tree

# litellm.set_verbose = True
import uuid 
session_id = str(uuid.uuid7())
async def run_agent_turn(available_tools: list, mcp_manager: McpManager):
    for _ in range(20):
        response = await acompletion(
            # model="anthropic/claude-sonnet-4-6",
            model="anthropic/claude-haiku-4-5",
            messages=messages,
            tools=available_tools,
            tool_choice="auto",
            temperature=0.2,
            metadata={
                "metadata": {
                    "session_id": session_id
                }
            }
        )

        if args.verbose:
            print("User prompt:", args.user_prompt)
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            messages.append(response_message.model_dump())
            for tool_call in tool_calls:
                if tool_call.function.name.startswith("mcp__"):
                    fn_res = await mcp_manager.call_mcp_tool(tool_call)
                else:
                    fn_res = call_function(tool_call, args.verbose)
                messages.append(fn_res)
        else:
            print(response_message.content)
            return True
    return False


from datetime import datetime, timezone
async def main():
    mcp_manager = McpManager()
    await mcp_manager.initialize()
    tools = mcp_manager.get_mcp_tools()
    available_tools.extend(tools)
    # limit to 20 exchanges to avoid excesive cost
    finished = await run_agent_turn(available_tools, mcp_manager)
    await mcp_manager.close()
    if not finished:
        print("Reached maximum number of iterations without finishing the conversation.")
        exit(1)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
asyncio.run(main())
