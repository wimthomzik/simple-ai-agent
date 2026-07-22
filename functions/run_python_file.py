import os, subprocess

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