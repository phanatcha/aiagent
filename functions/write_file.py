import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        parent_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
    
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {str(e)}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file (creates parent directories if needed). Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the target file (e.g., 'data/output.txt')",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file",
            ),
        },
        required=["file_path", "content"],  # Both parameters are mandatory
    ),
)