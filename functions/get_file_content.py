import os
from os import path


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        work_dir_abs = path.abspath(working_directory)
        norm_file_path = path.normpath(path.join(work_dir_abs, file_path))
        file_path_is_in_wd = os.path.commonpath([work_dir_abs, norm_file_path]) == work_dir_abs
        if not file_path_is_in_wd:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not path.isfile(norm_file_path):
            return f'Error: "{file_path}" is not a file'

        file = open(norm_file_path, 'r')
        content = file.read(10000)
        if file.read(1):
            content += f'[...File "{file_path}" truncated at 10000 character]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'
