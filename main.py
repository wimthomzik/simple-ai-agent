from dotenv import load_dotenv
import os, argparse
from openai import OpenAI
from prompts import system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import schema_get_files_content, get_file_content
from functions.write_file import write_file, schema_write_file


def init_llm_client():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if api_key is None:
        raise RuntimeError("Missing API key")
    
    return OpenAI(
        api_key=api_key, 
        base_url="https://openrouter.ai/api/v1"
        )
 
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt") 
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()
    
def main():
    
    client = init_llm_client()
    args = parse_args()
    
    available_function = [
        schema_write_file,
        schema_get_files_content,
        schema_get_files_info,
    ]
    
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]   
    
    response = client.chat.completions.create(model='openrouter/free', messages=messages, tools=available_function)
    prompt_tokens = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens
    
    if response_tokens is None:
        raise RuntimeError("Failed API request; no completion tokens received")
    
    if args.verbose == True:
        print(f"User prompt: {messages[-1]["content"]}")
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    print(f"Model response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
