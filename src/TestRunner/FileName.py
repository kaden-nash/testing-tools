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
    def __init__(self, path):
        self.path = path
    
    @property
    def extension(self):
        return os.path.splitext(self.path)[1][1:] # exclude dot
    
    @property
    def name(self):
        basename = os.path.basename(self.path)
        stop = len(basename) - len(self.extension) - 1
        return basename[:stop]