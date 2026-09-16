import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("api_key was not generated")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
prompt = "Why is Boot.dev such a great place to learn backend development? Use one sentence maximum."
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

def main():
    if response.usage == None:
        raise RuntimeError("responses usage property is None. Failed api request")

    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
