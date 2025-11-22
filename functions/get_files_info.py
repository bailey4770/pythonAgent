import os


def get_files_info(working_directory: str, directory="."):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory)) + os.sep

    if not full_path.startswith(working_directory + os.sep):
        return (
            None,
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory',
        )

    if not os.path.isdir(full_path):
        return None, f'Error: "{directory}" is not a directory'

    contents = os.listdir(full_path)
    res = []

    for item in contents:
        line = f" - {item}: file_size={os.path.getsize(full_path + item)} bytes, is_dir={os.path.isdir(full_path + item)}"
        res.append(line)

    return res, None
