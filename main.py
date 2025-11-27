import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.schemas import available_functions
from functions.utils import (
    get_files_info,
    get_file_content,
    write_file,
    run_python_file,
)

MODEL = "gemini-2.0-flash-001"
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
WORKING_DIRTORY = "./calculator"


def initialise_client():
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    return client


def get_user_prompt():
    args = sys.argv
    if len(args) <= 1:
        print("Error: please include arguments.")
        sys.exit(1)

    verbose = False
    prompt = None
    for arg in args:
        if arg == "--verbose":
            verbose = True
        else:
            prompt = arg

    if prompt == None:
        print("Error: please provide a prompt.")
        sys.exit(1)

    return prompt, verbose


def print_token_counts(response):
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    func_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call_part.name
    function_args = function_call_part.args

    if function_call_part.name not in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    func = func_dict[function_name]
    function_result = func(**function_args, working_directory=WORKING_DIRTORY)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def print_response(response):
    function_calls = response.function_calls

    if function_calls:
        for function_call_part in function_calls:
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )
    else:
        print(f"Response: \n {response.text}")


def main():
    client = initialise_client()

    prompt, verbose = get_user_prompt()

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )

    function_calls = response.function_calls
    function_calls_responses = []

    if function_calls:
        for function_call_part in function_calls:
            function_call_result = call_function(function_call_part, verbose)

            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError("Something went fatally wrong")
            else:
                function_calls_responses.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")


if __name__ == "__main__":

    main()
