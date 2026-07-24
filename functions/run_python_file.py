import os, subprocess

schema_run_python_file = {
    "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Executes a Python file within the working directory and returns its output (stdout, stderr, and exit code if non-zero). Optionally accepts command-line arguments to pass to the script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File-path to write content to, relative to the working directory",
                    },
                    "args": {
                        "type": "list[str]",
                        "description": "Contains command line arguments that are passed to the script",
                    },
                },
            },
        },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        is_valid_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
        
        if not is_valid_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        cmd = ["python", target_file]
        if args:
            cmd.extend(args)
        
        completed_process = subprocess.run(args=cmd, timeout=30., cwd=working_directory_abs, text=True, capture_output=True)

        string_out = []
        if completed_process.returncode != 0:
            string_out.append(f"Process exited with code {completed_process.returncode}")
        if completed_process.stderr is None and completed_process.stdout is None:
            string_out.append(f"\nNo output produced")
        else: 
            string_out.append(f"\nSTDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}")
        return "".join(string_out)
    except Exception as e:
        return f"Error: executing Python file: {e}"