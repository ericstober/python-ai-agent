import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    # Capture user input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # load environment variables from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Check for api key
    if not api_key:
        raise RuntimeError("API key issue")

    # Create new instance of a Gemini client
    client = genai.Client(api_key=api_key)

    # Create list of user's prompts
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Call Gemini client with model and prompt. Captured as response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # Check for token metadata
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    # If verbose output is enabled print metadata
    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Print response
    if response.function_calls:
        function_results = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if not function_call_result.parts:
                raise Exception("Function call result has no parts")

            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise Exception("Function call result has no function_response")

            if function_response.response is None:
                raise Exception("Function response has no response")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_response.response}")

    else:
        print(response.text)


if __name__ == "__main__":
    main()
