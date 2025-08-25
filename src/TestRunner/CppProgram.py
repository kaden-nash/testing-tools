from src.TestRunner.Program import Program
from src.TestRunner.FileName import FileName

class CppProgram(Program):
    def __init__(self, file: FileName):
        super().__init__(file)
    
    @property
    def executable_path(self):
        return f"{self.path[:-len(self.extension)]}exe"
        
    @property
    def run_command(self):
        return [f"{self.executable_path}"]

    @property
    def compilation_command(self):
        return ["g++", f"{self.path}", "-o", f"{self.executable_path}"]