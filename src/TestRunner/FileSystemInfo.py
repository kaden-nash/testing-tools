import os

class FileSystemInfo():
    """
    Contains information about the file system relevant to the script

    Attributes:
        cwd - string of current working directory (absolute)
        tests_dir - string of absolute path to tests directory from cwd
        project_file - string of valid filename

    """
    def __init__(self):
        self.cwd = self._get_cwd()
        self.tests_dir = self._get_tests_dir()

    def _get_cwd(self):
        return os.getcwd()

    def _get_tests_dir(self):
        return os.path.join(self.cwd, "tests")