from functions.get_file_contents import get_file_content

lorem_test = ["calculator", "lorem.txt"]
args = [
    ["calculator", "main.py"],
    ["calculator", "pkg/calculator.py"],
    ["calculator", "/bin/cat"],
    ["calculator", "pkg/does_not_exist.py"],
]

for arg in args:
    content, err = get_file_content(*arg)

    print(f"Showing result for args {arg}")
    if err:
        print(f"    {err}")
    else:
        print(content)
