from src.TestRunner.Program import Program
from src.TestRunner.FileName import FileName

class CppProgram(Program):
    """
    Child of Program class that contains information about a C++ program.

    Attributes:
        executable_path: str - absolute path to executable file (.exe)
        run_command: list - command arguments to run the compiled C++ program
        compilation_command: list - g++ command arguments to compile C++ program
    """
    def __init__(self, file: FileName):
        """
        Initialize C++ program with source file path.
        
        Args:
            file: FileName - FileName object containing C++ source file path
        """
        super().__init__(file)
    
    @property
    def executable_path(self):
        """
        Generate path for compiled executable.
        
        Returns:
            str: Path to .exe file (Windows-specific)
        """
        return f"{self.path[:-len(self.extension)]}exe"
        
    @property
    def run_command(self):
        """
        Get command to execute the compiled program.
        
        Returns:
            list: Command arguments for subprocess.run
        """
        return [f"{self.executable_path}"]

    @property
    def compilation_command(self):
        """
        Get g++ compilation command.
        
        Returns:
            list: g++ command arguments for subprocess.run
        """
        return ["g++", f"{self.path}", "-o", f"{self.executable_path}"]