import os
import sys
import subprocess
from src.TestRunner.FileLines import FileLines
from src.TestRunner.Program import Program
from src.TestRunner.FileSystemInfo import FileSystemInfo
from src.TestRunner.file_search import file_search

def create_test_files(environment: FileSystemInfo):
    """Execute testCreator.exe to generate test files.
    
    Creates test input/output files if they don't exist and handles
    any errors during the test creation process.
    
    Args:
        environment: FileSystemInfo containing test directory paths
    """
    test_creator_path = find_test_creator()

    first_time = False
    if not os.path.exists(environment.tests_dir):
        first_time = True
        print("\nThere are no test files yet... I'll create some...")

    output_object = subprocess.run(
        test_creator_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if output_object.returncode != 0:
        print(f"\nProblem running testCreator.exe:")
        print(f"{output_object.stderr}")
        exit(0)
    else:
        print(f"\nSuccessfully run testCreator.exe")

    if first_time:
        print(f"{output_object.stdout}There we go!\n")

def find_test_creator() -> str:
    """Locate the testCreator.exe executable.
    
    Returns:
        str: Absolute path to testCreator.exe in the TestCreator directory
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    executable_path = os.path.join(project_root, 'TestCreator', 'testCreator.exe')

    if getattr(sys, 'frozen', False):
        executable_path = os.path.join(sys._MEIPASS, "TestCreator", "testCreator.exe") # running in a PyInstaller bundle
    
    return executable_path

class SummaryData:
    """Data container for test execution summary information.
    
    Holds file paths, output data, and comparison metrics used
    throughout the test execution and summary generation process.
    """
    
    def __init__(self):
        """Initialize all summary data fields to default values."""
        self.expected_out_file = ""
        self.actual_out_file = ""
        self.in_file = ""
        self.summary_out_file = ""
        self.sumfile = None
        self.output_object = None
        self.actual_lines = None
        self.expected_lines = None
        self.extra_lines = 0
        self.mismatched_lines  = 0
        self.isMismatched = 0
        self.max_lines = 0
        self.i = 0

def compile_program(program: Program):
    """Compile the program if compilation is required.
    
    Args:
        program: Program instance containing compilation command
        
    Raises:
        SystemExit: If compilation fails
    """
    print("Testing your code...")
    output_object = subprocess.run(program.compilation_command, capture_output=True, text=True)

    # Handle compile errors
    if output_object.returncode != 0:
        print(f"\nProblem compiling {program.name}.{program.extension}:")
        print(f"{output_object.stderr}")
        exit(0)
    else:
        print(f"Successfully compiled {program.name}.{program.extension}")

def run_program(in_file: str, program: Program):
    """Execute the program with input from specified file.
    
    Args:
        in_file: Path to input file for program execution
        program: Program instance containing run command
        
    Returns:
        subprocess.CompletedProcess: Result of program execution
        
    Raises:
        SystemExit: If program execution fails
    """
    with open(in_file, "r") as in_filef:
        output_object = subprocess.run(program.run_command, stdin=in_filef, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Handle runtime errors/warnings
    if output_object.returncode != 0:
        print(f"\nProblem running {os.path.basename(in_file)}:")
        print(f"{output_object.stderr}")
        exit(0)
    else:
        print(f"Successfully run {program.name}.{program.extension} with {os.path.basename(in_file)}")
    
    return output_object

def write_to_output_file(sum_data: SummaryData):
    """Write program output to actual output file.
    
    Args:
        sum_data: SummaryData containing output and file paths
    """
    with open(sum_data.actual_out_file, "w") as actfile:
        sum_data.actual_lines = FileLines(sum_data.output_object.stdout.splitlines(keepends=True))
        for line in sum_data.actual_lines.raw:
            actfile.write(line)

def write_to_summary_file(sum_data: SummaryData):
    """Generate complete test summary file with output and comparisons.
    
    Args:
        sum_data: SummaryData containing all test execution information
    """
    sum_data.sumfile = open(sum_data.summary_out_file, "a")

    write_summary_header(sum_data)
    write_summary_output(sum_data)

    # Handle case where no expected output file exists
    if sum_data.expected_out_file == "":
        sum_data.i += 1
        write_summary_footer(sum_data)
        sum_data.sumfile.close()
        return

    write_summary_differences(sum_data)
    write_summary_matching_data(sum_data)
    write_summary_footer(sum_data)
    sum_data.sumfile.close()

def write_summary_header(sum_data: SummaryData):
    """Write header section of test summary with file paths."""
    # Add spacing between test cases
    if sum_data.i != 0:
        for _ in range(7):
            sum_data.sumfile.write(" " * 38)
            sum_data.sumfile.write("| |\n")

    sum_data.sumfile.write("------------------------------------------------------------------------------\n")
    sum_data.sumfile.write(f"Input from:     \t\t\t{sum_data.in_file}\nActual output from: \t\t{sum_data.actual_out_file}\n")
    if sum_data.expected_out_file != "":
        sum_data.sumfile.write(f"Expected output from:\t\t{sum_data.expected_out_file}\n")
    else:
        sum_data.sumfile.write("\t\t\t\t\t\t\tNo expected out file\n")

    sum_data.sumfile.write("---------------------------------------\n")

def write_summary_output(sum_data: SummaryData):
    """Write actual program output to summary file."""
    for line in sum_data.actual_lines.fancy:
        sum_data.sumfile.write(line)

def write_summary_differences(sum_data: SummaryData):
    """Analyze and write differences between actual and expected output."""
    write_difference_header(sum_data)

    with open(sum_data.expected_out_file, "r") as efile:
        sum_data.expected_lines = FileLines(efile.readlines())

    write_length_difference(sum_data)
    write_line_differences(sum_data)
    write_extra_lines(sum_data)

def write_difference_header(sum_data: SummaryData):
    """Write differences section header."""
    sum_data.isMismatched = 0

    sum_data.sumfile.write("---------------------------------------\n")
    sum_data.sumfile.write("Differences\n")
    sum_data.sumfile.write("---------------------------------------\n")

def write_length_difference(sum_data):
    """Compare and report differences in output length."""
    if len(sum_data.actual_lines.split) != len(sum_data.expected_lines.split):
        sum_data.isMismatched = 1
        sum_data.sumfile.write(f"Difference in actual and expected output lengths:\n\t\tactual length:    {len(sum_data.actual_lines.split)}\n\t\texpected length:  {len(sum_data.expected_lines.split)}\n\n")

def write_line_differences(sum_data: SummaryData) -> None:
    """Compare lines and report mismatches between actual and expected output."""
    k = 0
    holder = ""
    sum_data.mismatched_lines = 0
    for (aline, eline) in zip(sum_data.actual_lines.fancy, sum_data.expected_lines.fancy):
        if aline != eline:
            sum_data.mismatched_lines += 1
            k += 1
            holder += f"\tactual:  \t{aline}\texpected:\t{eline}\n"
    
    if k == 0:
        return
    
    sum_data.sumfile.write("Mismatched lines:\n")
    sum_data.sumfile.write(holder)

def write_extra_lines(sum_data: SummaryData):
    """Report extra lines in either actual or expected output."""
    if sum_data.isMismatched != 1:
        return

    sum_data.extra_lines = len(sum_data.actual_lines.split) - len(sum_data.expected_lines.split)

    if len(sum_data.actual_lines.split) > len(sum_data.expected_lines.split): 
        write_extra_actual_lines(sum_data)
    else: 
        write_extra_expected_lines(sum_data)

def write_extra_actual_lines(sum_data: SummaryData):
    """Write extra lines found in actual output."""
    sum_data.max_lines = len(sum_data.actual_lines.split)
    sum_data.sumfile.write("Extra lines in actual_out:\n")

    start = len(sum_data.actual_lines.split) - sum_data.extra_lines
    stop = len(sum_data.actual_lines.split)
    for j in range(start, stop): 
        line = sum_data.actual_lines.fancy[j]
        sum_data.sumfile.write(f"\t\t\t\t{line}")
    
def write_extra_expected_lines(sum_data: SummaryData):
    """Write extra lines found in expected output."""
    sum_data.max_lines = len(sum_data.expected_lines.split)
    sum_data.extra_lines *= -1
    sum_data.sumfile.write("Extra lines in expected_out:\n")

    start = len(sum_data.expected_lines.split) - sum_data.extra_lines
    stop = len(sum_data.expected_lines.split)
    for j in range(start, stop): 
        line = sum_data.expected_lines.fancy[j]
        sum_data.sumfile.write(f"\t\t\t\t{line}")

def write_summary_matching_data(sum_data: SummaryData) -> dict[str,]:
    """Calculate and write matching lines statistics."""
    sum_data.mismatched_lines += sum_data.extra_lines
    sum_data.sumfile.write(f"\nMatching lines: ({sum_data.max_lines - sum_data.mismatched_lines}/{sum_data.max_lines})\n")

def write_summary_footer(sum_data: SummaryData):
    """Write footer separator for test summary."""
    sum_data.sumfile.write("-----------------------------------------\n")
    
def create_file_wrappers(in_file: str, environment: FileSystemInfo, sum_data: SummaryData, expected_out_files: list):
    """Set up file paths for test execution and output comparison.
    
    Args:
        in_file: Path to input file for the test
        environment: FileSystemInfo containing test directory paths
        sum_data: SummaryData to populate with file paths
        expected_out_files: List of available expected output files
    """
    sum_data.in_file = in_file
    sum_data.actual_out_file = os.path.join(environment.tests_dir, f"actual_out{sum_data.i}.txt")
    sum_data.expected_out_file = os.path.join(environment.tests_dir, f"expected_out{sum_data.i}.txt")

    # Clear expected file path if it doesn't exist
    if sum_data.expected_out_file not in expected_out_files:
        sum_data.expected_out_file = ""