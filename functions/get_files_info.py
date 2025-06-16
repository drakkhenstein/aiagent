def get_files_info(working_directory, directory=None):
    """
    Get information about files in the specified directory.

    Args:
        working_directory (str): The base working directory.
        directory (str, optional): The specific directory to get file info from. Defaults to None.

    Returns:
        list: A list of dictionaries containing file information.
    """
    import os

    if directory is None:
        directory = working_directory
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
        for files in os.listdir(abs_directory):
            file_path = os.path.join(abs_directory, files)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            files_info.append(f"- {files}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: {str(e)}"

