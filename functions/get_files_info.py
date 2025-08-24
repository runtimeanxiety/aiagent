import os


def get_files_info(working_directory, directory="."):
    files_info = ""
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    full_path = os.path.join(working_directory, directory)

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside of the permitted working directory.'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory.'

    try:
        for file_name in os.listdir(target_dir):
            files_info += f"- {file_name}: file_size={os.path.getsize(os.path.join(full_path, file_name))} bytes, is_dir={os.path.isdir(os.path.join(full_path, file_name))}\n"
    except Exception as e:
        return f"Error: {e}"
