import re

class FileLines():
    """
    Class that takes in and manipulates raw lines from a file.

    Attributes:
        raw: list - Original lines passed in from file
        split: list - Lines and newlines separated for processing
        fancy: list - Lines formatted with delimiters for comparison output
    """
    def __init__(self, raw):
        """
        Initialize with raw file lines.
        
        Input:
            raw: list of strings - Raw lines from file (with line endings)
        """
        self.raw = raw
    
    @property
    def split(self):  # sourcery skip: use-getitem-for-re-match-groups
        """
        Parses program output, separating content from newlines for readability.

        Input:
            Uses self.raw - list of raw lines from file (with line endings)

        Output:
            list of strings - Lines and newlines as separate elements
        """

        final_lines = []

        for i, line in enumerate(self.raw):
            # get line
            text = re.search(r"([^\n]+)", line)

            # append
            if text != None:
                final_lines.append(text.group(1))
            else: # line is newline
                final_lines.append("\n")

            # if last line has newline, add extra newline (it just works and I forgot why)
            if i == len(self.raw) - 1 and "\n" in line:
                final_lines.append("\n")
        return final_lines

    @property
    def fancy(self):  # sourcery skip: assign-if-exp
        """
        Formats lines with delimiters for comparison printing.

        Input:
            Uses self.split - list of separated lines and newlines

        Output:
            list of strings - Lines formatted with --|content|-- delimiters
        """
        final_lines = []
        final_line = ""
        for line in self.split:
            if line == "\n":
                final_line = "--|\\n|--\n"
            else:
                final_line = f"--|{line}|--\n"
            final_lines.append(final_line)
        
        return final_lines