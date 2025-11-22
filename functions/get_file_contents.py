import os


def get_file_content(working_directory: str, file_path):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not (full_path + os.sep).startswith(working_directory + os.sep):
        return (
            None,
            f'Error: Cannot list "{file_path}" as it is outside the permitted working directory',
        )

    if os.path.isdir(full_path):
        return None, f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except:
        return None, f"Error: file does not exist"

    if len(file_content_string) == MAX_CHARS:
        file_content_string += '[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string, None
