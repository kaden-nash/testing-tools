import os

class FileSystemInfo():
    """
    Contains information about the file system relevant to the script.

    Attributes:
        cwd: str - Current working directory (absolute path)
        tests_dir: str - Absolute path to tests directory from cwd
    """
    def __init__(self):
        """Initialize FileSystemInfo instance."""
        pass
    
    @property
    def cwd(self):
        """
        Get current working directory.
        
        Returns:
            str: Absolute path of current working directory
        """
        return os.getcwd()

    @property
    def tests_dir(self):
        """
        Get path to testing files directory.
        
        Returns:
            str: Absolute path to 'testing_files' subdirectory
        """
        return os.path.join(self.cwd, "testing_files")