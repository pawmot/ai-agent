from functions.get_file_content import get_file_content

def call(wd, file):
    print(get_file_content(wd, file))


if __name__ == "__main__":
    call("calculator", "lorem.txt")
    call("calculator", "pkg/calculator.py")
    call("calculator", "main.py")
    call("calculator", "/bin/cat")
    call("calculator", "pkg/does_not_exist.py")


