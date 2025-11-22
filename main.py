import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


MODEL = "gemini-2.0-flash-001"


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


def main():
    client = initialise_client()

    prompt, verbose = get_user_prompt()

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    response = client.models.generate_content(model=MODEL, contents=messages)

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Response: {response.text}")
        print_token_counts(response)
    else:
        print(f"Response {response.text}")


if __name__ == "__main__":

    main()
