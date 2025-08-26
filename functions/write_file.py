import os
from google.genai import types


def write_file(working_directory, file_path, content):
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target_file):
        try:
            os.makedirs(os.path.dirname(abs_target_file), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(abs_target_file) and os.path.isdir(abs_target_file):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(abs_target_file, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file "{file_path}": {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Can write to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be writen to the file.",
            )
        },
        required=["file_path", "content"],
    ),
)