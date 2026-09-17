import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_directory_path, file_path))
        valid_target_path = os.path.commonpath([abs_working_directory_path, target_path]) == abs_working_directory_path

        if valid_target_path == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error listing files: {e}"