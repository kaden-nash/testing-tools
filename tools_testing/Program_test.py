import pytest

@pytest.mark.program
@pytest.mark.parametrize(
    "filepath",
    ["D:\\folder\\main.c"]
)
def test_program(filepath):
    from src.TestRunner.CProgram import CProgram
    from src.TestRunner.FileName import FileName
    prog = CProgram(FileName(filepath))
    assert prog.name == "main"