from langchain.tools import tool
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

work_dir = '.'


def set_working_directory(working_directory: str):
    global work_dir
    work_dir = working_directory


@tool("get_files_info")
def get_files_info_tool(directory: str = ".") -> str:
    """Lists files in a specified directory relative to the working directory, providing file name, size, and directory status

    Args:
        directory: Directory path to list files from, relative to the working directory (default is the working directory itself)
    """
    print("- Tool: get_files_info")
    return get_files_info(work_dir, directory)


@tool("get_file_content")
def get_file_content_tool(file_path: str) -> str:
    """Get the content of a file relative to the working directory

    Args:
        file_path: Path of the file to read, relative to the working directory
    """
    print("- Tool: get_file_content")
    return get_file_content(work_dir, file_path)


@tool("write_file")
def write_file_tool(file_path: str, content: str) -> str:
    """Write content to a file relative to the working directory. If the file already exists it will be overwritten. Returns the length of the content written to the file

    Args:
        file_path: Path of the file to write, relative to the working directory
        content: Content to write to the file
    """
    print("- Tool: write_file")
    return write_file(work_dir, file_path, content)


@tool("run_python_file")
def run_python_file_tool(file_path: str, arguments: list[str] | None = None) -> str:
    """Execute a Python file relative to the working directory. Optionally args may be passed. Returns the result code (if not zero), and the output - stdout and stderr (if present).

    Args:
        file_path: Path of the file to execute, relative to the working directory. The file MUST be a Python file ('.py' extension)
        arguments: Optional list of arguments to pass to the executed Python script
    """
    print("- Tool: run_python_file")
    return run_python_file(work_dir, file_path, arguments)
