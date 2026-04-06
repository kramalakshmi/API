import pathlib
def main():
    src_dir = pathlib.Path("src")
    test_dir = pathlib.Path("tests")
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / "test_create.py"
    commit_file(str(test_file), "Test")


if __name__ == "__main__":
    main()
