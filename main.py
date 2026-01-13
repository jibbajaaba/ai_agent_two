import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("api_key env variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generate_content(client, messages, args)

def generate_content(client, messages, args):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    prompt_tokens = response.usage_metadata.prompt_token_count
    candidates_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", candidates_tokens)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
