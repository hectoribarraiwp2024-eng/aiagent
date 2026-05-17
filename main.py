import os
from dotenv import load_dotenv
from google import genai
import argparse

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise Exception("the api_key was not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    prompt = args.user_prompt

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    if response.usage_metadata == None:
        raise RuntimeError("usage_metadata is None so the API request failed")

    p_tok = response.usage_metadata.prompt_token_count
    r_tok = response.usage_metadata.candidates_token_count
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {p_tok}")
    print(f"Response tokens: {r_tok}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
