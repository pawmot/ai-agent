import os
from os import path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_dir_abs = path.abspath(working_directory)
        norm_file_path = path.normpath(path.join(work_dir_abs, file_path))
        file_path_is_in_wd = os.path.commonpath([work_dir_abs, norm_file_path]) == work_dir_abs
        if not file_path_is_in_wd:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if path.isdir(norm_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = path.dirname(norm_file_path)
        if not path.exists(parent_dir):
            os.makedirs(parent_dir, 0o777, True)

        file = open(norm_file_path, 'w')
        _ = file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
