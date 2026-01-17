import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith("py"):
            return f'Error: "{file_path}" is not a Python file'
        print(target_file)
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        completed_command = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
            )
        if completed_command.returncode != 0:
            return f"Process exited with code {completed_command.returncode}"
        if completed_command.stdout is None or completed_command.stderr is None:
            return "No output produced"
        return f"STDOUT: {completed_command.stdout} \n STDERR: {completed_command.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"
