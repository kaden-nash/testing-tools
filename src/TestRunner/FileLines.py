import re

class FileLines():
    """
    Class that takes in and manipulates raw lines from a file.

    Attributes:
        raw - list of the lines passed in
        split - list of lines and newlines separated
        fancy - list of lines and newlines viable for printing to another file
    """
    def __init__(self, raw):
        self.raw = raw
    
    @property
    def split(self):  # sourcery skip: use-getitem-for-re-match-groups
        """
        Parses program output, reordering newlines for more readability

        Input:
            raw lines from a file (with ends)

        Output:
            list of string lines and string newlines separated
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
        Formats lines for comparsion printing

        Input:
            a line (string)

        Output:
            the string to print to summary_out.txt
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