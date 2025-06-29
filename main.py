import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.call_function import call_function
from config import MAX_ITERS

def main():
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieves the content of a specific file.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to retrieve content from, relative to the working directory.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file and returns the output.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a specific file.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write to, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
        ),
    ) 

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(args)
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    model_name = "gemini-2.0-flash-001"  # Default model, can be changed as needed
    

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached. Exiting.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose, model_name, available_functions)
            if final_response: 
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            
        
def generate_content(client, messages, verbose, model_name, available_functions):
    system_prompt = """
    You are a helpful AI coding agent that can autonomously explore and analyze code.

    When a user asks a question about code or a project, you should:
    1. First explore the directory structure to understand the project layout
    2. Read relevant files to understand the codebase
    3. Then provide a comprehensive answer based on your analysis

    You can perform the following operations:
    - List files and directories (start with the root directory)
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. Be proactive and explore the codebase to find the information needed to answer the user's question.
    """
    response = client.models.generate_content(
        #model='gemini-2.0-flash-001', contents=messages,
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    if verbose:
        print("Prompt tokens:", tokens_prompt := response.usage_metadata.prompt_token_count)
        print("Response tokens:", tokens_response := response.usage_metadata.candidates_token_count)
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    function_call_part = response.function_calls[0]
    function_call_result = call_function(function_call_part, verbose=verbose)
    if not (
        function_call_result.parts and
        hasattr(function_call_result.parts[0], "function_response") and
        getattr(function_call_result.parts[0].function_response, "response", None)
    ):
        raise Exception("No function response received. Please check the function call and try again.")
    if verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    function_responses.append(function_call_result.parts[0])
    messages.append(
        types.Content(
            role="tool",
            parts=function_responses,
        )
    )
    return None

if __name__ == "__main__":
    main()

