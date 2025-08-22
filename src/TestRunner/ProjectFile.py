import string

from src.TestRunner.FileSystemInfo import FileSystemInfo
from src.TestRunner.CProgram import CProgram
from src.TestRunner.JavaProgram import JavaProgram
from src.TestRunner.FileFoundOverload import FileFoundOverload
from src.TestRunner.Program import Program
from src.TestRunner.file_search import file_search
from src.TestRunner.ProgramFactory import ProgramFactory
from src.TestRunner.FileName import FileName

class ProjectFile():
    """
    Gets a valid project file from user

    Attributes:
        path - a valid absolute file path of project name
    """

    def __init__(self, file: FileName):
        self.file = file
        self._ProgFac = ProgramFactory()
        self.program_object = self._get_program_type()

    def _get_program_object(self):
        return self._ProgFac.create_program(self.file)
