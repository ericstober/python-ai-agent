import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        # Get absolute path of working directory
        abs_working_dir = os.path.abspath(working_directory)

        # Construct full path to the target directory
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        # Check if target directory falls within the absolute working directory
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if directory is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Initalize array to store files info
        files_info = []

        # Iterate over the files in the target directory
        for filename in os.listdir(target_dir):
            # Get name, file size, and whether it's a directory itself
            filepath = os.path.join(target_dir, filename)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)

            # Build string for each file
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        # Return the strings from the files_info array as one joined string
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"
