import json 
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_files_info import get_files_info

def call_function(tool_call, verbose: bool = False) -> dict:
    function_args = json.loads(tool_call.function.arguments or "{}")
    function_args["working_directory"] = "./calculator"
    function_name = tool_call.function.name
    function_id = tool_call.id
    
    if verbose:
        print(f"- Calling function: {tool_call.function.name}({function_args})")
    else:
        print(f"- Calling function: {tool_call.function.name}")
    
    match function_name:
        case "get_file_content":
            content = get_file_content(**function_args)
        case "get_files_info":
            content = get_files_info(**function_args)
        case "run_python_file":
            content = run_python_file(**function_args)
        case "write_file":
            content = write_file(**function_args)
        case _:
            content = f"Error: Unknown function: {function_name}"
            
    output = {
            "role": "tool",
            "tool_call_id": function_id,
            "content": content
        }    
        
    
    return output