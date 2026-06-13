import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory, creating or overwriting the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return (
                f'Error: Cannot write to "{file_path}" '
                "as it is outside the permitted working directory"
            )

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" ' "as it is a directory"

        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_path, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f"({len(content)} characters written)"
        )

    except Exception as e:
        return f"Error: {e}"
