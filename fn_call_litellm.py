from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
import json

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(tool_call, verbose: bool = False):
    if verbose:
        print(f' - Calling function: {tool_call.function.name}({tool_call.function.arguments})')
    else:
        print(f' - Calling function: {tool_call.function.name}')

    function_name = tool_call.function.name or ""
    function = function_map[function_name]
    if function is None:
        return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": { "error": f"Unknown function: {function_name}" }
        }
    
    args = dict(json.loads(tool_call.function.arguments)) if tool_call.function.arguments else {}
    args["working_directory"] = "./calculator"
    fun_res = function(**args)
    if verbose:
        print(f' - Function result: \n{fun_res}')
    return {
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": json.dumps({"result": fun_res }),
    }

