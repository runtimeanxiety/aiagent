import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory.'

    if not os.path.exists(target_dir):
        return f'Error: File "{file_path}" not found.'

    if not target_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python3", file_path] + args,
            capture_output=True,
            cwd=working_directory,
            timeout=30,
        )
        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout.decode()}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr.decode()}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
