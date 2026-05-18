import os

def write_file(working_directory, file_path, content):
    try:
        abs_wd = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_tp = os.path.commonpath([abs_wd, target_file]) == abs_wd

        if not valid_tp:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        with open(target_file, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing content: {e}"