import os

from google.genai import types


# used to get the info on a file, it's type and size and if its a file or folder
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


# schema to identify what this function is for ai agent.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
)
