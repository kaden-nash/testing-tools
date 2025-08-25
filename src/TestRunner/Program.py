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
    def __init__(self, file: FileName):
        self.name = file.name
        self.extension = file.extension
        self.path = file.path
    
    @property
    @abstractmethod
    def executable_path(self):
        pass
        
    @property
    @abstractmethod
    def run_command(self):
        pass

    @property
    @abstractmethod
    def compilation_command(self):
        pass
    
    def __str__(self):
        return self.path