from src.TestRunner.Program import Program
from src.TestRunner.FileName import FileName

class PythonProgram(Program):
    """
    Concrete implementation of Program for Python files.
    """
    
    def __init__(self, file: FileName):
        """Initialize Python program instance.
        
        Args:
            file: FileName object containing Python file details
        """
        super().__init__(file)

    @property
    def executable_path(self):
        """Get executable path for Python programs.
        
        Returns:
            None: Python doesn't produce separate executables
        """
        return None
        
    @property
    def run_command(self):
        """Get command to execute the Python program.
        
        Returns:
            str: Command string to run the Python file
        """
        return f"python {self.path}"

    @property
    def compilation_command(self):
        """Get compilation command for Python programs.
        
        Returns:
            None: Python is interpreted and doesn't require compilation
        """
        return None