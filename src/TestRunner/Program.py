from abc import ABC, abstractmethod
from src.TestRunner.FileName import FileName

class Program(ABC):
    """Abstract base class for executable programs in the test runner.
    
    Provides a common interface for different programming language executables,
    handling file metadata and defining required execution methods.
    """
    
    def __init__(self, file: FileName):
        """Initialize program with file information.
        
        Args:
            file: FileName object containing program file details
        """
        self.name = file.name
        self.extension = file.extension
        self.path = file.path
    
    @property
    @abstractmethod
    def executable_path(self):
        """Get the path to the executable for this program type."""
        pass
        
    @property
    @abstractmethod
    def run_command(self):
        """Get the command to execute this program."""
        pass

    @property
    @abstractmethod
    def compilation_command(self):
        """Get the command to compile this program if needed."""
        pass
    
    def __str__(self):
        """Return string representation of the program."""
        return self.path