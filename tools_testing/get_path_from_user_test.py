import pytest
from src.TestRunner.get_path_from_user import get_path_from_user, _isolate_file, _get_user_match_selection
import src.TestRunner.get_path_from_user

matches_temp = [
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\CProgram.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\file_search.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\FileFoundOverload.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\FileLines.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\FileName.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\FileSystemInfo.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\get_path_from_user.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\JavaProgram.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\Main.py",
    "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\MainHelpers.py",
]

@pytest.mark.l1
@pytest.mark.parametrize(
    "mock_user_inputs, matches, expected",
    [
        ([".py", "CProgram.py"], [matches_temp, [matches_temp[0]]], "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\CProgram.py"),
        (["z", "CProgram.py"], [[], [matches_temp[0]]], "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\CProgram.py"),
    ]
)
def test_get_path_from_user(mock_user_inputs, matches, expected, monkeypatch):
    from src.TestRunner.FileSystemInfo import FileSystemInfo
    sysinfo = FileSystemInfo()

    i = iter(mock_user_inputs)
    def mock_user_input(prompt):
        return next(i)

    j = iter(matches)
    def mock_potential_matches(cwd, matches1):
        return next(j)

    monkeypatch.setattr("builtins.input", mock_user_input)
    monkeypatch.setattr(src.TestRunner.get_path_from_user, "file_search", mock_potential_matches)
    
    assert get_path_from_user(sysinfo) == expected



@pytest.mark.l2
@pytest.mark.parametrize(
    "mock_user_inputs, expected_match",
    [
        ("1", "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\CProgram.py"),
        ("2", "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\file_search.py"),
        ("3", "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\FileFoundOverload.py"),
        ("4", "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\FileLines.py"),
    ]
)
def test_isolate_file(mock_user_inputs, expected_match, get_matches, monkeypatch):
    i = iter(mock_user_inputs)
    def mock_input(prompt):
        return next(i)
    monkeypatch.setattr("builtins.input", mock_input)
    assert _isolate_file(get_matches) == expected_match



@pytest.mark.l3
@pytest.mark.parametrize(
    "input_string, expected_index",
    [
        (["g", "y", "2"], 2),
        (["11", "3"], 3),
        (["0", "1"], 1),
        (["g", "c", "1"], 1), # expect fail due to terminating function
        ("9", 9) 
    ]
)
def test_get_user_match_selection(input_string, expected_index, get_matches, monkeypatch):
    it = iter(input_string)
    def mock_input(prompt):
        return next(it)
    monkeypatch.setattr("builtins.input", mock_input)

    assert _get_user_match_selection(get_matches) == expected_index