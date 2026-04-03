import os
from os import path
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        work_dir_abs = path.abspath(working_directory)
        norm_file_path = path.normpath(path.join(work_dir_abs, file_path))
        file_path_is_in_wd = os.path.commonpath([work_dir_abs, norm_file_path]) == work_dir_abs
        if not file_path_is_in_wd:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not path.isfile(norm_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not norm_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", norm_file_path]
        if args:
            command.extend(args)

        completed = subprocess.run(command, cwd=work_dir_abs, capture_output=True, text=True, timeout=30)
        result = ""
        if completed.returncode != 0:
            result += f'Process exited with code {completed.returncode}\n'
        output = ""
        if completed.stdout:
            output += f'STDOUT: {completed.stdout}\n'
        if completed.stderr:
            output += f'STDERR: {completed.stderr}\n'
        if not output:
            output = "No output produced\n"
        result += output
        return result
    except Exception as e:
        return f'Error: executing Python file {str(e)}'
