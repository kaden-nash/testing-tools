from src.TestRunner.Program import Program

class CProgram(Program):
    """
    Child of Program class that contains information about a C program.

    Attributes:
        executable_path: str - absolute path to executable file (.exe)
        run_command: list - command arguments to run the compiled C program
        compilation_command: list - gcc command arguments to compile C program
    """
    def __init__(self, file):
        """
        Initialize C program with source file path.
        
        Args:
            file: str - path to C source file
        """
        super().__init__(file)

    @property    
    def executable_path(self):
        """
        Generate path for compiled executable.
        
        Returns:
            str: Path to .exe file (Windows-specific)
        """
        # Currently Windows-specific (.exe extension)
        return f"{self.path[:-len(self.extension)]}exe"
        # TODO: Add cross-platform support for .out files on Unix systems

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
        Get gcc compilation command with math library linking.
        
        Returns:
            list: gcc command arguments for subprocess.run
        """
        return ["gcc", f"{self.path}", "-lm", "-o", f"{self.executable_path}"]