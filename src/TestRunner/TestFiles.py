from src.TestRunner.FileSystemInfo import FileSystemInfo
from src.TestRunner.file_search import file_search

class TestFiles():
    """
    Finds existing test files

    Attributes:
        search_term - the search term/prefix for test files this class will find. 
    
    """
    def __init__(self, search_term):
        self._system_info = FileSystemInfo()
        self.files = self.get_files(search_term)
    
    def get_files(self, search_term):
        matches = file_search(self._system_info.tests_dir, search_term)
        matches.sort()
        return matches