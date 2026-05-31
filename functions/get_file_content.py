import os

MAX_CHARS = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return (
                f'Error: Cannot read "{file_path}" as it is outside '
                f"the permitted working directory"
            )

        if not os.path.isfile(abs_file_path):
            return f"Error: File not found or is not a regular file: " f'"{file_path}"'

        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at ' f"{MAX_CHARS} characters]"
                )

        return content

    except Exception as e:
        return f"Error: {e}"
