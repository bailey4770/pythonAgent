import os
import subprocess


def _check_path_in_working_directory(working_directory, path):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, path))

    if not (full_path + os.sep).startswith(working_directory + os.sep):
        raise LookupError

    return full_path


def get_files_info(working_directory: str, directory="."):
    try:
        full_path = (
            _check_path_in_working_directory(working_directory, directory) + os.sep
        )
    except LookupError:
        raise Exception(
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )

    if not os.path.isdir(full_path):
        raise Exception(f'Error: "{directory}" is not a directory')

    contents = os.listdir(full_path)
    res = []

    for item in contents:
        line = f" - {item}: file_size={os.path.getsize(full_path + item)} bytes, is_dir={os.path.isdir(full_path + item)}"
        res.append(line)

    return res


def get_file_content(working_directory: str, file_path):
    try:
        full_path = _check_path_in_working_directory(working_directory, file_path)
    except LookupError:
        raise Exception(
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        )

    if os.path.isdir(full_path):
        raise Exception(
            f'Error: File not found or is not a regular file: "{file_path}"'
        )

    MAX_CHARS = 10000

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        raise Exception(e)

    if len(file_content_string) == MAX_CHARS:
        file_content_string += '[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string


def write_file(working_directory, file_path, content):
    try:
        full_path = _check_path_in_working_directory(working_directory, file_path)
    except LookupError:
        raise Exception(
            f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        )

    dir_path = os.path.dirname(full_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = _check_path_in_working_directory(working_directory, file_path)
    except LookupError:
        raise Exception(
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        )

    if not os.path.exists(full_path):
        raise Exception(f'Error: File "{file_path}" not found.')

    if not file_path.endswith(".py"):
        raise Exception(f'Error: "{file_path}" is not a Python file.')

    try:
        result = subprocess.run(
            ["python", full_path, *args], capture_output=True, timeout=30, text=True
        )

        if not (result.stderr + result.stdout).strip():
            return "No output produced."

        return f"STDOUT: {result.stdout} \nSTDERR: {result.stderr}\n==============="

    except Exception as e:
        raise Exception(f"Error: executing Python file: {e}")
