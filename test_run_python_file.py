from functions.run_python_file import run_python_file

def call(wd, file, args=None):
    print(run_python_file(wd, file, args))


if __name__ == "__main__":
    call("calculator", "main.py")
    call("calculator", "main.py", ["3 + 5"])
    call("calculator", "tests.py")
    call("calculator", "../main.py")
    call("calculator", "nonexistent.py")
    call("calculator", "lorem.txt")

