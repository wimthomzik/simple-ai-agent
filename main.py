from dotenv import load_dotenv
import os
from openai import OpenAI

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if api_key is None:
        raise RuntimeError("Missing API key")
    
    client = OpenAI(
        api_key=api_key, 
        base_url="https://openrouter.ai/api/v1"
        )
    
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
    
    response = client.chat.completions.create(model='openrouter/free', messages=messages)
    prompt_tokens = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens
    
    if response_tokens is None:
        raise RuntimeError("Failed API request; no completion tokens received")
    
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
