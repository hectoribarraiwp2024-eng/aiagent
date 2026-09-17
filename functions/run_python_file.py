import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_directory_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_directory_path, file_path))
        valid_target_path = os.path.commonpath([abs_working_directory_path, target_path]) == abs_working_directory_path

        if valid_target_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args:
            command.extend(args)

        subpro = subprocess.run(
            command, cwd=abs_working_directory_path, capture_output=True,
            text=True, timeout=30
            )

        result = []

        if subpro.returncode != 0:
            result.append(f"Process exited with code {subpro.returncode}")
        if not subpro.stdout and not subpro.stderr:
            result.append("No output produced")
        if subpro.stdout:
            result.append(f"STDOUT:\n{subpro.stdout}")
        if subpro.stderr:
            result.append(f"STDERR:\n{subpro.stderr}")

        return "\n".join(result)

    except Exception as e:
        return f"Error: executing Python file: {e}"