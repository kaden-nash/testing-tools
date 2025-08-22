import pytest

@pytest.mark.parametrize(
    "filepath, expected_name, expected_extension",
    [
        ("C:/Users/Example/Documents/file.txt", "file", "txt"),
        ("C:\\Users\\main.program.c", "main.program", "c"),
        ("C:/Users/Main.java", "Main", "java")
    ]
    )
def test_name_and_extension(filepath, expected_name, expected_extension):
    from src.TestRunner.FileName import FileName
    file = FileName(filepath)
    assert file.name == expected_name
    assert file.extension == expected_extension