import argparse
parser = argparse.ArgumentParser(description="Chatbot")
_ = parser.add_argument("user_prompt", type=str, help="User prompt")
_ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

from dotenv import load_dotenv
_ = load_dotenv()

from fn_langchain import get_files_info_tool, get_file_content_tool, write_file_tool, run_python_file_tool, set_working_directory
set_working_directory('./calculator')
local_tools = [get_files_info_tool, get_file_content_tool, write_file_tool, run_python_file_tool]


from langchain_litellm import ChatLiteLLM
llm = ChatLiteLLM(model="anthropic/claude-haiku-4-5", temperature=0.2)

mcp_servers = {
    "add": {
        "transport": "stdio",
        "command": "uv",
        "args": ["run", "main.py"],
        "cwd": "./mcp_servers/add"
    },
    "power": {
        "transport": "http",
        "url": "http://localhost:8123/mcp"
    }
}
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.interceptors import ToolCallInterceptor, MCPToolCallRequest
class LogMcpToolCall(ToolCallInterceptor):
    async def __call__(self, request: MCPToolCallRequest, handler):
        print(f"- MCP Tool call: {request.name}")
        return await handler(request)

mcp_client = MultiServerMCPClient(mcp_servers, tool_interceptors=[LogMcpToolCall()])

from langchain.agents import create_agent
from langchain.messages import SystemMessage
from prompts import system_prompt

from langchain.messages import HumanMessage

async def main():
    mcp_tools = await mcp_client.get_tools()
    tools = local_tools + mcp_tools
    agent = create_agent(llm, system_prompt=SystemMessage(system_prompt), tools=tools)
    response = await agent.ainvoke({"messages":HumanMessage(args.user_prompt)})
    print(response["messages"][-1].content)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
