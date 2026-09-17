import os
import argparse
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
from config import system_prompt
from call_functions import available_functions, call_function
def main():
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("api_key was not generated")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages_list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for i in range(20):
        generate_response(client, messages_list, args.verbose)
        if i == 20:
            print("Exiting the loop maxiterations has been made")
            sys.exit(1)

def generate_response(client, messages_list, verbose):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages_list,
        tools=available_functions,
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    message = response.choices[0].message
    messages_list.append(message)

    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        messages_list.append(result_message)
        if not result_message.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")


if __name__ == "__main__":
    main()
