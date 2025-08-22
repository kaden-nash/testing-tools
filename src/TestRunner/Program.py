from abc import ABC, abstractmethod
from src.TestRunner.FileName import FileName

class Program(ABC):
    """
    Class that holds information about a program that will be tested by this script.

    Precondition:
        Assumes that the file_path passed in is valid

    Attributes:
        path - string of file_path passed in
        name - string of file_name without extension
        extension - string of file extension
    """
    def __init__(self, path):
        self.path = path
        self.file = FileName(path)
    
    @abstractmethod
    @property    
    def executable_path(self):
        pass
        
    @abstractmethod
    @property
    def run_command(self):
        pass

    @abstractmethod
    @property
    def compilation_command(self):
        pass
    
    def __str__(self):
        return self.path