from functions.utils import get_file_content

lorem_test = ["calculator", "lorem.txt"]
args = [
    ["calculator", "main.py"],
    ["calculator", "pkg/calculator.py"],
    ["calculator", "/bin/cat"],
    ["calculator", "pkg/does_not_exist.py"],
]

for arg in args:
    try:
        content = get_file_content(*arg)
        print(f"Showing result for args {arg}")
        print(content)

    except Exception as e:
        print(f"Error {e}")
