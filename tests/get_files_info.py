from functions.utils import get_files_info

test_args = [
    ["calculator", "."],
    ["calculator", "pkg"],
    ["calculator", "/bin"],
    ["calculator", "../"],
]

for args in test_args:
    try:
        received = get_files_info(*args)

        if args[1] == ".":
            print("Result for current directory:")
        else:
            print(f"Result for {args[1]} directory:")

        print("\n".join(received))

    except Exception as e:
        print(f"Error: {e}")
