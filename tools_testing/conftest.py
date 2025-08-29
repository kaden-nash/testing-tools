import pytest
from src.TestRunner.FileSystemInfo import FileSystemInfo

@pytest.fixture
def get_matches() -> list:
    return [
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
        "D:\\Testing-Tools\\testing-tools\\src\\TestRunner\\Program.py",
    ]