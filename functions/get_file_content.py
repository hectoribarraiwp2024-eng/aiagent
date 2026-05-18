import os 
from config import CHAR_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_wd = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_tp = os.path.commonpath([abs_wd, target_file]) == abs_wd

        if not valid_tp:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, 'r') as f:
            doc = f.read(CHAR_LIMIT)
            if f.read(1):
                doc += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
        return doc



    except Exception as e:
        return f"Error reading files: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads file in a specified file path relative to the working directory, providing 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to read contents from, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)