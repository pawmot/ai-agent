from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description = "Lists files in a specified directory relative to the working directory, providing file name, size, and directory status",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)"
            )
        }
    )
)

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Get the content of a file relative to the working directory",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read, relative to the working directory"
            )
        },
        required=["file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Write content to a file relative to the working directory. If the file already exists it will be overwritten. Returns the length of the content written to the file",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file"
            )
        },
        required=["file_path", "content"]
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Execute a Python file relative to the working directory. Optionally args may be passed. Returns the result code (if not zero), and the output - stdout and stderr (if present).",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to execute, relative to the working directory. The file MUST be a Python file ('.py' extension)"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the executed Python script"
            )
        },
        required=["file_path"]
    )
)
