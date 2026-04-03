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

from litellm import completion
from prompts import system_prompt
messages = [
    {"role": "system", "content": [{ "type": "text", "text": system_prompt }]},
    {"role": "user", "content": [{ "type": "text", "text": args.user_prompt }]}
]
from fn_decl_litellm import schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
available_tools = [schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
from fn_call_litellm import call_function
finished = False
# limit to 20 exchanges to avoid excesive cost
# import litellm
# litellm.set_verbose = True
for _ in range(20):
    response = completion(
        # model="anthropic/claude-sonnet-4-6",
        model="anthropic/claude-haiku-4-5",
        messages=messages,
        tools=available_tools,
        tool_choice="auto",
        temperature=0.2,
    )

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        messages.append(response_message)
        for tool_call in tool_calls:
            fn_res = call_function(tool_call, args.verbose)
            messages.append(fn_res)
    else:
        print(response_message.content)
        finished = True
        break
if not finished:
    print("Reached maximum number of iterations without finishing the conversation.")
    exit(1)


