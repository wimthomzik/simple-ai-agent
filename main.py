from dotenv import load_dotenv
from openai import OpenAI
import os, argparse, sys
from prompts import system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import schema_get_files_content, get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from call_function import call_function
from config import MAX_ITERS

load_dotenv()

def init_llm_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
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
        schema_run_python_file
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
    
    if args.verbose == True:
                print(f"User prompt: {messages[-1]["content"]}")
    
    for _ in range(MAX_ITERS):
        try:
            response = client.chat.completions.create(model='openrouter/free', messages=messages, tools=available_function)
            
            if not response.usage:
                raise RuntimeError("API response appears to be malformed")
            
            if args.verbose:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
                        
            message = response.choices[0].message
            messages.append(message)
            
            tool_calls = message.tool_calls
            
            if not tool_calls:
                print("Final response:")
                print(message.content)
                return
            
            for tool_call in tool_calls:
                if tool_call.type != "function":
                    continue
                result_message = call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise RuntimeError(f"Empty function response for {tool_call.function.name}")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
                    
        except Exception as e:
            print(f"Error: {e}")
            
    print(f"Agent loop hit max. iterations ({MAX_ITERS})")
    sys.exit(-1)

if __name__ == "__main__":
    main()
