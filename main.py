import os, argparse
from dotenv import load_dotenv
from google import genai


def main():
    # Capture user input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    # load environment variables from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Check for api key
    if not api_key:
        raise RuntimeError("API key issue")

    # Create new instance of a Gemini client
    client = genai.Client(api_key=api_key)

    # Call Gemini client with model and prompt. Captured as response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt,
    )

    # Check for token metadata
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    # Print token metadata
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Print response
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
