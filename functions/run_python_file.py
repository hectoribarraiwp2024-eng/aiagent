import os 
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_wd = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_tp = os.path.commonpath([abs_wd, target_file]) == abs_wd

        if not valid_tp:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        commands = ["python", target_file]
        if args:
            commands.extend(args)

        result = subprocess.run(commands, capture_output=True, cwd=abs_wd, timeout=None, text=True)

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"