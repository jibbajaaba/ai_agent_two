import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f"Error: Cannot list {directory} as it is outside the permitted working directory"
        if not os.path.isdir(target_dir):
            return f"Error: {directory} is not a directory"
        file_info = []
        for item in os.listdir(target_dir):
            filepath = os.path.join(target_dir, item)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            file_info.append(
                f"- {item}: file size={file_size}, is_dir={is_dir}"
            )
        return "\n".join(file_info)
    except Exception as e:
        return f"Error: listing files: {e}"
