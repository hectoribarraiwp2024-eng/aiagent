import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from config import SYSTEM_PROMPT
from call_function import available_functions, call_function
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise Exception("the api_key was not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    prompt = args.user_prompt
    for i in range(20):
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages, 
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT, temperature=0),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata == None:
            raise RuntimeError("usage_metadata is None so the API request failed")

        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return

        function_responses = []
        for function_call in response.function_calls:
            result = call_function(function_call, args.verbose)
            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])
        
            messages.append(types.Content(role="user", parts=function_responses))

        if i == 19:
            print('the program already looped 20 times something went wrong')
            sys.exit(1)

        

if __name__ == "__main__":
    main()
