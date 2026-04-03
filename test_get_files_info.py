from functions.get_files_info import get_files_info

def call(wd, dir):
    print(f'Result for {"current" if dir == "." else dir} directory:')
    print("  " + get_files_info(wd, dir).replace("\n", "\n  "))


if __name__ == "__main__":
    call("calculator", ".")
    call("calculator", "pkg")
    call("calculator", "/bin")
    call("calculator", "../")


