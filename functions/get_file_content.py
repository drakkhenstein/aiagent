import os

def get_file_content(working_directory, file_path):
    """
    Get the content of a file in the specified working directory.

    Args:
        working_directory (str): The base working directory.
        file_path (str): The path to the file relative to the working directory.

    Returns:
        str: The content of the file or an error message if the file cannot be accessed.
    """
    

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000

    try:
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            content = file.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS]
                content += f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f"Error: {str(e)}"

    
