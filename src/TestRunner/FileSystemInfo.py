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
        pass
    
    @property
    def cwd(self):
        return os.getcwd()

    @property
    def tests_dir(self):
        return os.path.join(self.cwd, "testing_files")