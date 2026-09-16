import os

def get_files_info(working_directory, directory="."):
    try:    
        abs_working_directory_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_directory_path, directory))
        valid_target_path = os.path.commonpath([abs_working_directory_path, target_path]) == abs_working_directory_path
        
        if valid_target_path == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        if valid_target_path:
            return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"
    