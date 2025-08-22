class FileFoundOverload(Exception):
    """
    Too many matching files found in file search

    Attributes:
        message -- explanation of the error
        code -- optional error code
    """

    def __init__(self, message, code=None):
        super().__init__(message)  # Call the base class constructor
        self.message = message
        self.code = code

    def __str__(self):
        if self.code:
            return f"FileFoundOverload (Code {self.code}): {self.message}"
        else:
            return f"FileFoundOverload: {self.message}"