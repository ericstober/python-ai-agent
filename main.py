import os
from dotenv import load_dotenv
from google import genai


def main():
    # load environment variables from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Check for api key
    if not api_key:
        raise RuntimeError("API key issue")

    # Create new instance of a Gemini client
    client = genai.Client(api_key=api_key)

    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )

    print(res.text)


if __name__ == "__main__":
    main()
