import os
import subprocess
from src.TestRunner.FileLines import FileLines
from src.TestRunner.Program import Program
from src.TestRunner.FileSystemInfo import FileSystemInfo
from src.TestRunner.file_search import file_search

def create_test_files(environment: FileSystemInfo):
    """
    Runs testCreator.exe
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, 'TestCreator', 'testCreator.exe')

class SummaryData:
    def __init__(self):
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
    # compile code (if necessary)
    print("Testing your code...")
    output_object = subprocess.run(program.compilation_command, capture_output=True, text=True)

    # handle compile errors
    if output_object.returncode != 0:
        print(f"\nProblem compiling {program.name}.{program.extension}:")
        print(f"{output_object.stderr}")
        exit(0)
    else:
        print(f"Successfully compiled {program.name}.{program.extension}")

def run_program(in_file: str, program: Program):
    # run code
    with open(in_file, "r") as in_filef:
        output_object = subprocess.run(program.run_command, stdin=in_filef, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # handle runtime errors/warnings
    if output_object.returncode != 0:
        print(f"\nProblem running {os.path.basename(in_file)}:")
        print(f"{output_object.stderr}")
        exit(0)
    else:
        print(f"Successfully run {program.name}.{program.extension} with {os.path.basename(in_file)}")
    
    return output_object

def write_to_output_file(sum_data: SummaryData):
    with open(sum_data.actual_out_file, "w") as actfile:
        sum_data.actual_lines = FileLines(sum_data.output_object.stdout.splitlines(keepends=True))
        for line in sum_data.actual_lines.raw:
            actfile.write(line)

def write_to_summary_file(sum_data: SummaryData):  # sourcery skip: ensure-file-closed
        sum_data.sumfile = open(sum_data.summary_out_file, "a")

        write_summary_header(sum_data)

        write_summary_output(sum_data)

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
    for line in sum_data.actual_lines.fancy:
        sum_data.sumfile.write(line)

def write_summary_differences(sum_data: SummaryData):
    write_difference_header(sum_data)

    with open(sum_data.expected_out_file, "r") as efile:
        sum_data.expected_lines = FileLines(efile.readlines())

    write_length_difference(sum_data)

    write_line_differences(sum_data)

    write_extra_lines(sum_data)

def write_difference_header(sum_data: SummaryData):
    # write differences (if there were any)
    sum_data.isMismatched = 0

    sum_data.sumfile.write("---------------------------------------\n")
    sum_data.sumfile.write("Differences\n")
    sum_data.sumfile.write("---------------------------------------\n")

def write_length_difference(sum_data):
    if len(sum_data.actual_lines.split) != len(sum_data.expected_lines.split):
        sum_data.isMismatched = 1
        sum_data.sumfile.write(f"Difference in actual and expected output lengths:\n\t\tactual length:    {len(sum_data.actual_lines.split)}\n\t\texpected length:  {len(sum_data.expected_lines.split)}\n\n")

def write_line_differences(sum_data: SummaryData) -> None:
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
    if sum_data.isMismatched != 1:
        return

    sum_data.extra_lines = len(sum_data.actual_lines.split) - len(sum_data.expected_lines.split)

    if len(sum_data.actual_lines.split) > len(sum_data.expected_lines.split): 
        write_extra_actual_lines(sum_data)
    else: 
        write_extra_expected_lines(sum_data)

def write_extra_actual_lines(sum_data: SummaryData):
    sum_data.max_lines = len(sum_data.actual_lines.split)
    sum_data.sumfile.write("Extra lines in actual_out:\n")

    start = len(sum_data.actual_lines.split) -sum_data.extra_lines
    stop = len(sum_data.actual_lines.split)
    for j in range(start, stop): 
        line = sum_data.actual_lines.fancy[j]
        sum_data.sumfile.write(f"\t\t\t\t{line}")
    
def write_extra_expected_lines(sum_data: SummaryData):
    sum_data.max_lines = len(sum_data.expected_lines.split)
    sum_data.extra_lines *= -1
    sum_data.sumfile.write("Extra lines in expected_out:\n")

    start = len(sum_data.expected_lines.split) -sum_data.extra_lines
    stop = len(sum_data.expected_lines.split)
    for j in range(start, stop): 
        line = sum_data.expected_lines.fancy[j]
        sum_data.sumfile.write(f"\t\t\t\t{line}")

def write_summary_matching_data(sum_data: SummaryData) -> dict[str,]:
    sum_data.mismatched_lines += sum_data.extra_lines
    sum_data.sumfile.write(f"\nMatching lines: ({sum_data.max_lines - sum_data.mismatched_lines}/{sum_data.max_lines})\n")

def write_summary_footer(sum_data: SummaryData):
    sum_data.sumfile.write("-----------------------------------------\n")
    
def create_file_wrappers(in_file: str, environment: FileSystemInfo, sum_data: SummaryData, expected_out_files: list):
    sum_data.in_file = in_file
    sum_data.actual_out_file = os.path.join(environment.tests_dir, f"actual_out{sum_data.i}.txt")
    sum_data.expected_out_file = os.path.join(environment.tests_dir, f"expected_out{sum_data.i}.txt")

    if sum_data.expected_out_file not in expected_out_files:
        sum_data.expected_out_file = ""