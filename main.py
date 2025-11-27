import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.schemas import available_functions


MODEL = "gemini-2.0-flash-001"
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


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

    if verbose:
        print(f"User prompt: {prompt}")
        print_response(response)
        print_token_counts(response)
    else:
        print_response(response)


if __name__ == "__main__":

    main()
