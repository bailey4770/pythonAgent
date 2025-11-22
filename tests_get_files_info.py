from functions.get_files_info import get_files_info

test_args = [
    ["calculator", "."],
    ["calculator", "pkg"],
    ["calculator", "/bin"],
    ["calculator", "../"],
]

for args in test_args:
    received, err = get_files_info(*args)

    if args[1] == ".":
        print("Result for current directory:")
    else:
        print(f"Result for {args[1]} directory:")

    if err:
        print(f"    {err}")
    else:
        print("\n".join(received))
