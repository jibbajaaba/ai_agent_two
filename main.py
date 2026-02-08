import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import system_prompt
from functions.call_functions import available_functions, call_function


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

    # loop for agent to make function calls
    for _ in range(20):
        response = generate_content(client, messages, args)

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_response_parts = []
            for function_call in response.function_calls:
                function_response = call_function(function_call, args.verbose)
                if function_response.parts == []:
                    raise Exception("parts should not be an empty list")
                part = function_response.parts[0]

                function_response_parts.append(part)

            messages.append(types.Content(role="user", parts=function_response_parts))

            continue

        print("Final Response")
        print(response.text)
        return

    print("Agent failed to produce a final reponse")
    sys.exit(1)


# function to generate the content for agent to use
def generate_content(client, messages, args):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
            )
    )

    return response


if __name__ == "__main__":
    main()
