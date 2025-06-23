from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part, verbose=False):
    """
    Calls the specified function with the provided arguments.
    
    Args:
        function_call_part: The function call part containing the function name and arguments.
        verbose (bool): If True, prints additional debug information.
    
    Returns:
        The result of the function call.
    """
    # Extract the function name and arguments
    function_name = function_call_part.name
    args = function_call_part.args
        
    # Dynamically get the function from the current module
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    function = function_map.get(function_name)
    if not function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(args)
    args["working_directory"] = "./calculator"

    # Call the function with the provided arguments
    result = function(**args)
        
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
    
