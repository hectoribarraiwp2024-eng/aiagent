import os

def get_files_info(working_directory, directory="."):
    try:    
        abs_working_directory_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_directory_path, directory))
        valid_target_path = os.path.commonpath([abs_working_directory_path, target_path]) == abs_working_directory_path
        
        if valid_target_path == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        files_info = []
        for filename in os.listdir(target_path):
            filepath = os.path.join(target_path, filename)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)

    except Exception as e:
        return f"Error listing files: {e}"
    