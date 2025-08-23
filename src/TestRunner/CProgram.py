from src.TestRunner.Program import Program

class CProgram(Program):
    """
    Child of Program class that contains information about a C program.

    Attributes:
        executable_path - absolute path to executable file
        run_command - list of strings to be passed to subprocess.run to run C program
        compilation_command - list of strings be passed to subprocess.run to compile C program
    """
    def __init__(self, file):
        super().__init__(file)

    @property    
    def executable_path(self):
        # if get_shell_type() == "powershell":
        return f"{self.path[:-len(self.extension)]}.exe"
        # elif get_shell_type() == "bash":
        #     self.executable = self.name + ".out"
    @property
    def run_command(self):
        return [f"{self.executable_path}"]
    @property
    def compilation_command(self):
        return ["gcc", f"{self.path}", "-lm", "-o", f"{self.executable_path}"]