from src.TestRunner.Program import Program

class JavaProgram(Program):
    """
    Concrete implementation of Program for Java files.
    """
    
    def __init__(self, file):
        """Initialize Java program instance.
        
        Args:
            file: FileName object containing Java file details
        """
        super().__init__(file)
    
    @property
    def executable_path(self):
        """Get path to the compiled .class file.
        
        Returns:
            str: Path to the .class file that will be created after compilation
        """
        return f"{self.path[:-len(self.extension)]}class"
    
    @property
    def run_command(self):
        """Get command to execute the compiled Java program.
        
        Returns:
            list: Command arguments for running the Java program via JVM
        """
        return ["java", f"{self.path}"]

    @property
    def compilation_command(self):
        """Get command to compile the Java source file.
        
        Returns:
            list: Command arguments for compiling Java source to bytecode
        """
        return ["javac", f"{self.path}"]