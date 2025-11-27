from functions.utils import run_python_file

test_cases = [
    ["calculator", "main.py"],
    ["calculator", "main.py", ["3 + 5"]],
    ["calculator", "tests.py"],
    ["calculator", "../main.py"],
    ["calculator", "nonexistent.py"],
    ["calculator", "lorem.txt"],
]

for test in test_cases:
    try:
        res = run_python_file(*test)
        print(res)
    except Exception as e:
        print(e)
