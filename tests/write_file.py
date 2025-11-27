from functions.utils import write_file

tests = [
    ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
    ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
    ["calculator", "/tmp/temp.txt", "this should not be allowed"],
]

for test in tests:
    try:
        res = write_file(*test)
        print(res)
    except Exception as e:
        print(e)
