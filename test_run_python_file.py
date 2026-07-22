from functions.run_python_file import run_python_file

def main():
    print(run_python_file("calculator", "main.py"))            # usage instructions
    print(run_python_file("calculator", "main.py", ["3 + 5"])) # runs a calculation
    print(run_python_file("calculator", "tests.py"))           # calculator's tests pass
    print(run_python_file("calculator", "../main.py"))         # error
    print(run_python_file("calculator", "nonexistent.py"))     # error
    print(run_python_file("calculator", "lorem.txt"))          # error
    
    
if __name__ == "__main__":
    main()