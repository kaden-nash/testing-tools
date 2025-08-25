from src.TestRunner.Program import Program
from src.TestRunner.CProgram import CProgram
from src.TestRunner.JavaProgram import JavaProgram
from src.TestRunner.PythonProgram import PythonProgram
from src.TestRunner.CppProgram import CppProgram
from src.TestRunner.FileName import FileName

class ProgramFactory():
    def __init__(self, path):
        self.file = FileName(path)
        self.supported_languages = {
            "c": CProgram,
            "java": JavaProgram,
            "py": PythonProgram,
            "cpp": CppProgram
        }
    
    def create_program(self) -> Program:
        if self.file.extension in self.supported_languages:
            return self.supported_languages[self.file.extension](self.file)

        print(f"Unsupported file: \"{self.file.extension}\" - terminating.")
        exit(0)