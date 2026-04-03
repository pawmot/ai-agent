import json

FUNCTION = "function"
OBJECT = "object"
STRING = "string"
ARRAY = "array"

def denone(dict):
    return {k: v for k, v in dict.items() if v is not None}

def function_parameters(params=None, required=None):
    return denone({
        "type": OBJECT,
        "properties": params,
        "required": required,
    })

def function_parameter(type, description, items_type=None):
    return denone({
        "type": type,
        "items": { "type": items_type } if items_type else None,
        "description": description
    })

def items_type(type):
    return {
        "type": type
    }

def function_declaration(name: str, description: str, parameters):
    return denone({
        "type": FUNCTION,
        "function": denone({
            "name": name,
            "description": description,
            "parameters": parameters
        })
    })

schema_get_files_info = function_declaration(
    name = "get_files_info",
    description = "Lists files in a specified directory relative to the working directory, providing file name, size, and directory status",
    parameters = function_parameters(
        params = {
            "directory": function_parameter(
                type = STRING,
                description = "Directory path to list files from, relative to the working directory (default is the working directory itself)"
            )
        }
    )
)

schema_get_file_content = function_declaration(
    name = "get_file_content",
    description = "Get the content of a file relative to the working directory",
    parameters = function_parameters(
        params={
            "file_path": function_parameter(
                type=STRING,
                description="Path of the file to read, relative to the working directory"
            )
        },
        required=["file_path"]
    )
)

schema_write_file = function_declaration(
    name = "write_file",
    description = "Write content to a file relative to the working directory. If the file already exists it will be overwritten. Returns the length of the content written to the file",
    parameters = function_parameters(
        params={
            "file_path": function_parameter(
                type=STRING,
                description="Path of the file to write, relative to the working directory"
            ),
            "content": function_parameter(
                type=STRING,
                description="Content to write to the file"
            )
        },
        required=["file_path", "content"]
    )
)

schema_run_python_file = function_declaration(
    name = "run_python_file",
    description = "Execute a Python file relative to the working directory. Optionally args may be passed. Returns the result code (if not zero), and the output - stdout and stderr (if present).",
    parameters = function_parameters(
        params={
            "file_path": function_parameter(
                type=STRING,
                description="Path of the file to execute, relative to the working directory. The file MUST be a Python file ('.py' extension)"
            ),
            "args": function_parameter(
                type=ARRAY,
                items_type=STRING,
                description="Optional list of arguments to pass to the executed Python script"
            )
        },
        required=["file_path"]
    )
)
