import os
from google.genai import types


def get_file_content(working_directory, file_path):

    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.join(abs_working_dir, file_path)
    abs_target_file = os.path.abspath(target_file)

    if not abs_target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_target_file, 'r') as f:
            content = f.read(10000)
            if os.path.getsize(abs_target_file) > 10000:
                content += f'[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Can return the content of a file up to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read content from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)