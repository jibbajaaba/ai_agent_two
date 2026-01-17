from functions.run_python_code import run_python_file


def test():

    result = run_python_file("calculator", "main.py")
    print("Results from test")
    print(result)

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Results from test")
    print(result)

    result = run_python_file("calculator", "tests.py")
    print("Results from test")
    print(result)

    result = run_python_file("calculator", "../main.py")
    print("Results from test")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print("Results from test")
    print(result)

    result = run_python_file("calculator", "lorem.txt")
    print("Results from test")
    print(result)


if __name__ == "__main__":
    test()
