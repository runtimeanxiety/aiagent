import os


def get_files_info(working_directory, directory="."):
    files_info = ""
    full_path = os.path.join(working_directory, directory)

    if (
        os.path.abspath(full_path).startswith(os.path.abspath(working_directory))
        is False
    ):
        return f'Error: Cannot list "{directory}" as it is outside of the permitted working directory.'

    if os.path.isdir(full_path) is False:
        return f'Error: "{directory}" is not a directory.'

    try:
        for file_name in os.listdir(full_path):
            files_info += f"- {file_name}: file_size={os.path.getsize(os.path.join(full_path, file_name))} bytes, is_dir={os.path.isdir(os.path.join(full_path, file_name))}\n"
    except Exception as e:
        return f"Error: {e}"

    return files_info
