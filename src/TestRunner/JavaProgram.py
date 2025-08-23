from src.TestRunner.Program import Program

class JavaProgram(Program):
    """
    Child of Program class that contains information about a Java program.

    Attributes:
        executable_path - absolute path to executable file
        run_command - list of strings to be passed to subprocess.run to run Java program
        compilation_command - list of strings be passed to subprocess.run to compile Java program
    """
    def __init__(self, file):
        super().__init__(file)
    
    @property
    def executable_path(self):
        return f"{self.path[:-len(self.extension)]}.class"
    
    @property
    def run_command(self):
        return ["java", f"{self.path}"]

    @property
    def compilation_command(self):
        return ["javac", f"{self.path}"]