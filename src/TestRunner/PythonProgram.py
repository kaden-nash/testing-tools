from src.TestRunner.Program import Program
from src.TestRunner.FileName import FileName

class PythonProgram(Program):
    def __init__(self, file: FileName):
        super().__init__(file)

    @property
    def executable_path(self):
        return None
        
    @property
    def run_command(self):
        return f"python {self.path}"

    @property
    def compilation_command(self):
        return None