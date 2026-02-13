import os

from google.genai import types


# used to get the content of a file.
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


# schema to identify what this function is for ai agent.
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file in the working directory and return the content of the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            )
        },
        required=["file_path"]
    )
)

# sets up available functions to be used by ai agent
available_functions = types.Tool(
    function_declarations=[schema_get_file_content]
)
