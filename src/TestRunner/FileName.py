import os

# Omitted code for YAGNI purposes
# from abc import abstractmethod, ABC
# class FileNameSource(ABC):
#     @abstractmethod
#     @property
#     def extension(self):
#         pass

#     @abstractmethod
#     @property
#     def name(self):
#         pass

class FileName:
    """Extracts name and extension components from file paths."""
    
    def __init__(self, path):
        """
        Initialize with file path.
        
        Args:
            path: File path to parse
        """
        self.path = path
    
    @property
    def extension(self):
        """
        Get file extension without the dot.
        
        Returns:
            str: File extension (e.g., 'py', 'txt')
        """
        return os.path.splitext(self.path)[1][1:]  # exclude dot
    
    @property
    def name(self):
        """
        Get filename without extension.
        
        Returns:
            str: Base filename without extension
        """
        basename = os.path.basename(self.path)
        stop = len(basename) - len(self.extension) - 1
        return basename[:stop]