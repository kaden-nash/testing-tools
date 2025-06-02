# FIXME: MAKE SURE YOU DON'T TURN THIS FILE INTO AN EXE WITHOUT MAKING A COPY!!
# FIXME: DO THIS
# FIXME: DON'T IGNORE TOP

#TODO: Implement valgrind output to terminal if it doesn't match

import subprocess
import os
import string
import re

class Program():
    """
    Class that holds information about a program that will be tested by this script.

    Precondition:
        Assumes that the file_path passed in is valid

    Attributes:
        file_path - string of file_path passed in
        file_name - string of file_name without extension
        extension - string of file extension
    """
    def __init__(self, path):
        self.path = path
        (self.name, self.extension) = self._get_name_and_extension()

    def _get_name_and_extension(self):
        """
        Retrieves a file's extension

        Input:
            an absolute filepath

        Output:
            the name of a file and its extension at the end of the filepath
        """
        filename = os.path.basename(self.path) # get basename
        name_and_extension = []

        temp = filename[::-1] # reverse basename
        temp = temp.split('.', 1) # split at extension .
        for part in temp:
            name_and_extension.append(part[::-1]) # push to new list each item of temp reversed
        
        name_and_extension = name_and_extension[::-1] # reverse order of extension and file basename
        
        return name_and_extension[0], name_and_extension[1]
    
    def __str__(self):
        return self.path

class CProgram(Program):
    """
    Child of Program class that contains information about a C program.

    Attributes:
        executable_path - absolute path to executable file
        run_command - list of strings to be passed to subprocess.run to run C program
        compilation_command - list of strings be passed to subprocess.run to compile C program
    """
    def __init__(self, file_path):
        super().__init__(file_path)
        self.executable_path = self._get_executable_path();
        self.run_command = self._get_run_command()
        self.compilation_command = self._get_compilation_command()

    def _get_executable_path(self):
        # if get_shell_type() == "powershell":
        return self.path[:-len(self.extension)] + ".exe"
        # elif get_shell_type() == "bash":
        #     self.executable = self.name + ".out"

    def _get_run_command(self):
        return [f"{self.executable_path}"]

    def _get_compilation_command(self):
        return ["gcc", f"{self.path}", "-lm", "-o", f"{self.executable_path}"]

class JavaProgram(Program):
    """
    Child of Program class that contains information about a Java program.

    Attributes:
        executable_path - absolute path to executable file
        run_command - list of strings to be passed to subprocess.run to run Java program
        compilation_command - list of strings be passed to subprocess.run to compile Java program
    """
    def __init__(self, file_path):
        super().__init__(file_path)
        self.executable_path = self._get_executable_path()
        self.run_command = self._get_run_command()
        self.compilation_command = self._get_compilation_command()
    
    def _get_executable_path(self):
        return self.path[:-len(self.extension)] + ".class"
    
    def _get_run_command(self):
        return ["java", f"{self.path}"]

    def _get_compilation_command(self):
        return ["javac", f"{self.path}"]

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
        self.split = self._get_split()
        self.fancy = self._get_fancy()
    
    def _get_split(self):
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
            if i == len(self.raw) - 1:
                if "\n" in line:
                    final_lines.append("\n")

        return final_lines

    def _get_fancy(self):
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

class FileFoundOverload(Exception):
    """
    Too many matching files found in file search

    Attributes:
        message -- explanation of the error
        code -- optional error code
    """

    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        if self.code:
            return f"FileFoundOverload (Code {self.code}): {self.message}"
        else:
            return f"FileFoundOverload: {self.message}"

class FileSystemInfo():
    """
    Contains information about the file system relevant to the script

    Attributes:
        cwd - string of current working directory (absolute)
        tests_dir - string of absolute path to tests directory from cwd
        project_file - string of valid filename

    """
    def __init__(self):
        self.cwd = self._get_cwd()
        self.tests_dir = self._get_tests_dir()

    def _get_cwd(self):
        return os.getcwd()

    def _get_tests_dir(self):
        return os.path.join(self.cwd, "tests")
    
    def get_shell_type():
        """
        Determines whether the script is running in PowerShell or Bash.

        Returns:
            "powershell", "bash", or "unknown"
        """

        if os.name == 'nt':  # Windows
            if 'powershell.exe' in os.environ.get('COMSPEC', '').lower():
                return "powershell"
            elif 'bash.exe' in os.environ.get('COMSPEC', '').lower():
                return "bash" #bash through WSL
            elif 'bash' in os.environ.get('SHELL', '').lower():
                return "bash" #git bash
            else:
                return "unknown"  # Could be cmd.exe or another shell
        elif os.name == 'posix':  # Linux/macOS
            if 'bash' in os.environ.get('SHELL', '').lower():
                return "bash"
            elif 'zsh' in os.environ.get('SHELL', '').lower():
                return "bash" #zsh is very similar to bash, and generally treated the same for most purposes.
            else:
                return "unknown" #other posix shell
        else:
            return "unknown"  # Other operating systems
            
class ProjectFile():
    """
    Gets a valid project file from user

    Attributes:
        path - a valid absolute file path of project name
    """

    def __init__(self):
        self._system_info = FileSystemInfo()
        self.path = self._get_valid_name()
        self.type = self._get_file_type(Program(self.path))

    def _get_file_type(self, file):
        if file.extension == "c":
            return CProgram(file.path)
        
        if file.extension == "java":
            return JavaProgram(file.path)

    def _get_valid_name(self):
        """
        Gets valid project_file path

        Output:
            valid project_file path
        """
        file = None
        valid_name_found = False
        while valid_name_found == False:
            # get name
            path = False
            if path == False:
                path = input("Enter name of file to test: ")

            # find potential matches
            potential_matches = file_search(self._system_info.cwd, path)
            
            user_choice = ""
            try: # isolate one file
                file = self._isolate_file(potential_matches)

            except FileNotFoundError as e: # choice: exit or enter different filename
                print(f"Error occurred: {e.args[0]}\n\n")
                user_choice = input("Enter filename again or exit[C]: ")

                if user_choice == "C" or user_choice == "c":
                    print("Exiting program.")
                    exit(0)
                else:
                    path = user_choice
                    continue
                
            except FileFoundOverload as e: # choice: exit or enter different filename
                print(f"Error occurred: {e.args[0]}\n\n")
                user_choice = input("(you'll probably want to exit and switch to a different cwd) Enter filename again or exit[C]: ")

                if user_choice in "Cc":
                    print("Exiting program.")
                    exit(0)
                else: # return singular found file
                    path = user_choice
                    continue

            else:
                valid_name_found = True
                # print("Located file.")
                
        
        return file
    
    def _isolate_file(self, matches):
        """
        Isolates a single file of a queue containing potential_name

        Input:
            List of absolute filepaths with string potential_file_name in them

        Output: 
            None if one file could not be isolated, absolute filepath match if it could be isolated
        """

        # determine action based on number of potential matches
        match = None
        if len(matches) == 0:
            raise FileNotFoundError("The specified file could not be found. Please ensure you are in the right cwd.")
        elif len(matches) == 1:
            match = matches[0]
        elif len(matches) == 10:
            raise FileFoundOverload("9+ files were found matching. Please ensure you are in the right cwd.")
        else:
            correctIndex = self._user_selection(matches) - 1
            match = matches[correctIndex]
        
        return match

    def _user_selection(self, matches):
        """
        Takes user selection of correct file out of 10 possible found items.

        Input:
            list of matches

        Output: 
            index + 1 of place in list that has the right filepath
        """

        print("More than one file found.")
       
       # print matches
        for i, match in enumerate(matches):
            if i > 9:
                break

            print(f"[{i+1}] - {match}") 
        
        # get valid input
        isValid = False
        match_index = ""
        while (isValid == False):
            match_index = input("Please enter the number next to the correct file or enter C to cancel: ")

            # check for non letters or digits
            invalid_input = False
            for ltr in match_index:
                if ltr not in "Cc" and ltr not in string.digits:
                    invalid_input = True
                    break
                
            # exit if user cancelled
            if match_index in "Cc":
                exit(0)

            if invalid_input == True:
                continue

            # check for numbers outside range
            if int(match_index) <= len(matches) and int(match_index) >= 1:
                isValid = True
        
        return int(match_index) # is 1-10, not 0-9

class TestFiles():
    """
    Finds existing test files

    Attributes:
        search_term - the search term/prefix for test files this class will find. 
    
    """
    def __init__(self, search_term):
        self._system_info = FileSystemInfo()
        self.files = self._get_files(search_term)
    
    def _get_files(self, search_term):
        matches = file_search(self._system_info.tests_dir, search_term)
        matches.sort()
        return matches

def file_search(root_dir, searchTerm):
        """
        Searches for a file 

        Input:
            absolute directory path to begin searching through, a string term to search for

        Output:
            list of all files from root_dir and lower containing the search_term in their names
        """
        matches = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
                for filename in filenames:
                    if searchTerm in filename:
                        full_path = os.path.join(dirpath, filename)
                        matches.append(full_path)

        return matches

def create_test_files():
    """
    Runs testCreator.exe
    """

    print("\nThere are no test files yet... I'll create some...")
    output_object = subprocess.run([f"./testCreator.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if output_object.returncode != 0:
        print(f"\nProblem running testCreator.exe:")
        print(f"{output_object.stderr}")
        exit(0)
    else:
        print(f"\nSuccessfully run testCreator.exe")
    
    print(f"{output_object.stdout}There we go!\n")



def main():
    """
    Drives script
    """

    # program variables
    project_file = ProjectFile()
    program_info = project_file.type
    environment = FileSystemInfo()

    # testing variables
    if not os.path.exists(environment.tests_dir):
        create_test_files()
    
    in_files = TestFiles("in").files
    actual_out_files = TestFiles("actual_out").files
    expected_out_files = TestFiles("expected_out").files
    summary_out_file = os.path.join(environment.tests_dir, "output_summary.txt")

    # helper variables
    actual_lines = None
    expected_lines = None
    max_lines = 0
    mismatched_lines = 0
    i = 0

    # compile code (if necessary)
    print("Testing your code...")
    output_object = subprocess.run(program_info.compilation_command, capture_output=True, text=True)

    # handle compile errors
    if output_object.returncode != 0:
        print(f"\nProblem compiling {program_info.name}.{program_info.extension}:")
        print(f"{output_object.stderr}")
        exit(0)
    else:
        print(f"Successfully compiled {program_info.name}.{program_info.extension}")

    # clear previous data in output_summary.txt
    with open(summary_out_file, "w") as sumfile:
        pass
    
    # compare files
    for in_file in in_files:
        actual_out_file = os.path.join(environment.tests_dir, "actual_out" + f"{i}" + ".txt")
        expected_out_file = os.path.join(environment.tests_dir, "expected_out" + f"{i}" + ".txt")

        # get expected_out_file if it exists
        if expected_out_file not in expected_out_files:
            expected_out_file = ""
        
        # run code
        with open(in_file, "r") as in_filef:
            output_object = subprocess.run(program_info.run_command, stdin=in_filef, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # handle runtime errors/warnings
        if output_object.returncode != 0:
            print(f"\nProblem running {os.path.basename(in_file)}:")
            print(f"{output_object.stderr}")
            exit(0)
        else:
            print(f"Successfully run {program_info.name}.{program_info.extension} with {os.path.basename(in_file)}")
        
        # write output to actual output files
        with open(actual_out_file, "w") as actfile:
            actual_lines = FileLines(output_object.stdout.splitlines(keepends=True))
            for line in actual_lines.raw:
                actfile.write(line)
        
        # write summary of run information
        with open(summary_out_file, "a") as sumfile:
            mismatched_lines = 0

            if i != 0:
                for _ in range(7):
                    sumfile.write(" " * 38)
                    sumfile.write("| |\n")
                
            sumfile.write("------------------------------------------------------------------------------\n")
            sumfile.write(f"Input from:     \t\t\t{in_file}\nActual output from: \t\t{actual_out_file}\n")
            if expected_out_file != "":
                sumfile.write(f"Expected output from:\t\t{expected_out_file}\n")
            else:
                sumfile.write("\t\t\t\t\t\t\tNo expected out file\n")

            sumfile.write("---------------------------------------\n")
            
            for line in actual_lines.fancy:
                sumfile.write(line)

            if expected_out_file == "":
                i += 1
                continue

            # write differences (if there were any)
            isMismatched = 0

            sumfile.write("---------------------------------------\n")
            sumfile.write("Differences\n")
            sumfile.write("---------------------------------------\n")

            # open expected out flie
            with open (expected_out_file, "r") as efile:
                expected_lines = FileLines(efile.readlines())
            
            if len(actual_lines.split) != len (expected_lines.split):
                isMismatched = 1
                sumfile.write(f"Difference in actual and expected output lengths:\n\t\tactual length:    {len(actual_lines.split)}\n\t\texpected length:  {len(expected_lines.split)}\n\n")
        
            # write line differences to summary out
            sumfile.write("Mismatched lines:\n")
            for (aline, eline) in zip(actual_lines.fancy, expected_lines.fancy):
                if aline != eline:
                    mismatched_lines += 1
                    sumfile.write(f"\tactual:  \t{aline}\texpected:\t{eline}\n")

            # print extra lines
            if isMismatched == 1:
                extra_lines = len(actual_lines.split) - len(expected_lines.split)
                
                # actual is longer
                if len(actual_lines.split) > len(expected_lines.split): 
                    max_lines = len(actual_lines.split)
                    sumfile.write("Extra lines in actual_out:\n")

                    start = len(actual_lines.split) -extra_lines
                    stop = len(actual_lines.split) # -1?
                    for j in range(start, stop): 
                        line = actual_lines.fancy[j]
                        sumfile.write(f"\t\t\t\t{line}")
                        
                # expected is longer
                else: 
                    max_lines = len(expected_lines.split)
                    extra_lines *= -1
                    sumfile.write("Extra lines in expected_out:\n")

                    start = len(expected_lines.split) -extra_lines
                    stop = len(expected_lines.split) # -1?
                    for j in range(start, stop): 
                        line = expected_lines.fancy[j]
                        sumfile.write(f"\t\t\t\t{line}")

            # write num of matchking lines
            mismatched_lines += extra_lines
            sumfile.write(f"\nMatching lines: ({max_lines - mismatched_lines}/{max_lines})\n")
            sumfile.write("-----------------------------------------\n")

        i += 1

    print("\nAll done! See output_summary.txt in the \"tests\" folder for the testing summary.")
main()