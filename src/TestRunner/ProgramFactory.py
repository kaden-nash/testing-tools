from src.TestRunner.Program import Program
from src.TestRunner.CProgram import CProgram
from src.TestRunner.JavaProgram import JavaProgram
from src.TestRunner.PythonProgram import PythonProgram
from src.TestRunner.CppProgram import CppProgram
from src.TestRunner.FileName import FileName

class ProgramFactory():
    """Factory class for creating Program instances based on file extension.
    
    Supports multiple programming languages and provides a unified interface
    for creating appropriate Program subclasses.
    """
    
    def __init__(self, path):
        """Initialize factory with a file path.
        
        Args:
            path: File path to create a program instance for
        """
        self.file = FileName(path)
        # Map file extensions to their corresponding Program classes
        self.supported_languages = {
            "c": CProgram,
            "java": JavaProgram,
            "py": PythonProgram,
            "cpp": CppProgram
        }
    
    def create_program(self) -> Program:
        """Create appropriate Program instance based on file extension.
        
        Returns:
            Program: Concrete Program subclass instance for the file type
            
        Raises:
            SystemExit: If file extension is not supported
        """
        if self.file.extension in self.supported_languages:
            return self.supported_languages[self.file.extension](self.file)

        print(f"Unsupported file: \"{self.file.extension}\" - terminating.")
        exit(0)