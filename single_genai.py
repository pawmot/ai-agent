import os
from dotenv import load_dotenv
from prompts import system_prompt

_ = load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("Gemini API key not configured")

import argparse

parser = argparse.ArgumentParser(description="Chatbot")
_ = parser.add_argument("user_prompt", type=str, help="User prompt")
_ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

from google import genai
from google.genai import types
from fn_decl_genai import schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
from fn_call_genai import call_function

client = genai.Client(api_key=api_key)
available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
)
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
finished = False
# limit to 20 exchanges to avoid excesive cost
for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
            )
        )

    if response.candidates is not None and len(response.candidates) > 0:
        messages.extend([c.content for c in response.candidates if c.content is not None])

    if args.verbose:
        print('User prompt:', args.user_prompt)
        print('Prompt tokens:', response.usage_metadata.prompt_token_count)
        print('Response tokens:', response.usage_metadata.candidates_token_count)

    if response.function_calls:
        fun_responses = []
        for function_call in response.function_calls:
            fun_res = call_function(function_call, args.verbose)
            if fun_res.parts is None or len(fun_res.parts) == 0:
                raise RuntimeError(f'Function {function_call.name} did not return any result')
            if fun_res.parts[0].function_response is None:
                raise RuntimeError(f'Function {function_call.name} did not return a function response')
            if fun_res.parts[0].function_response.response is None:
                raise RuntimeError(f'Function {function_call.name} did not return a response in the function response')
            fun_responses.append(fun_res.parts[0])
        if args.verbose:
            print('\n'.join([f'{r.function_response.response}' for r in fun_responses]))

        messages.append(types.Content(role="user", parts=fun_responses))
    else:
        print(response.text)
        finished = True
        break
if not finished:
    print("Reached maximum number of iterations without finishing the conversation.")
    exit(1)

