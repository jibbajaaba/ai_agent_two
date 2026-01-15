import os


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f"Error: Cannot read {file_path} as it is outside the permitted working directory"
        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: {file_path}"
        with open(target_file) as file_to_read:
            content = file_to_read.read(10000)
            if file_to_read.read(1):
                content += (
                    f"[...File {file_path} truncated at 1000 characters]"
                )
        return content
    except Exception as e:
        return f"Error reading file {file_path}: {e}"
