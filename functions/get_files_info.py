import os
from os import path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        wd = path.abspath(working_directory)
        target_dir = path.normpath(path.join(wd, directory))
        target_dir_is_valid = os.path.commonpath([wd, target_dir]) == wd
        if not target_dir_is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        contents = [f'- {entry}: file_size={path.getsize(path.join(target_dir, entry))}, is_dir={path.isdir(path.join(target_dir, entry))}' for entry in os.listdir(target_dir)]

        return '\n'.join(contents)
    except Exception as e:
        return f'Error: {str(e)}'

