from src.TestRunner.CProgram import CProgram
from src.TestRunner.JavaProgram import JavaProgram
from src.TestRunner.FileName import FileName

class ProgramFactory():
    def __init__(self, file: FileName):
        self.file = file
        self.supported_languages = {
            "c": CProgram,
            "java": JavaProgram
        }
    
    def create_program(self):
        if self.file.extension in self.supported_languages:
            return self.supported_languages[self.file.extension](self.file.path)
        else:
            raise ValueError(f"Unsupported file extension: {self.file.extension}")
