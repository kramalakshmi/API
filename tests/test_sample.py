# 1. Syntax error
def test_syntax_error(
    assert True

# 2. Import error
from src.nonexistent import missing_fn

# 3. Wrong sys.path manipulation
import sys
sys.path.insert(0, "wrong_path")

# 4. NameError
def test_name_error():
    result = addd(1, 2)  # typo: addd

# 5. Wrong function signature
def test_wrong_signature():
    result = divide(1)  # missing second argument

# 6. Wrong expected value
def test_wrong_expected_value():
    assert add(1, 2) == 100

# 7. Missing exception test
def test_missing_exception():
    divide(1, 0)  # should use pytest.raises

# 8. Wrong fixture usage
def test_bad_fixture(nonexistent_fixture):
    assert True

# 9. Test that never executes source code
def test_no_execution():
    assert True

# 10. Test that crashes before running
def test_crash():
    raise RuntimeError("crash before running")

# 11. Duplicate/conflicting sys.path logic
sys.path.insert(0, "another_wrong_path")

# 12. Test for non-existent file
def test_file_not_found():
    open("no_such_file.txt").read()

# 13. Global state dependency
GLOBAL_LIST = []
def test_global_state():
    GLOBAL_LIST.append(1)
    assert GLOBAL_LIST == [1]

# 14. Incorrect testing of __main__
def test_main_block():
    import src.sample
    src.sample.__main__()
