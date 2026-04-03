from functions.write_file import write_file

def call(wd, file, content):
    print(write_file(wd, file, content))


if __name__ == "__main__":
    call("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    call("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    call("calculator", "/tmp/temp.txt", "this should not be allowed")


