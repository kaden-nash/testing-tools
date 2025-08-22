import os
import subprocess
from src.TestRunner.FileLines import FileLines
from src.TestRunner.Program import Program
from src.TestRunner.FileSystemInfo import FileSystemInfo

def create_test_files():
    """
    Runs testCreator.exe
    """

    print("\nThere are no test files yet... I'll create some...")
    output_object = subprocess.run(
        ["./testCreator.exe"],
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

    print(f"{output_object.stdout}There we go!\n")


class SummaryData:
    def __init__(self):
        self.expected_out_file = ""
        self.actual_out_file = ""
        self.in_file = ""
        self.summary_out_file = ""
        self.output_object = None
        self.actual_lines = None
        self.expected_lines = None
        self.extra_lines = 0
        self.mismatched_lines  = 0
        self.isMismatched = 0
        self.max_lines = 0
        self.i = 0

def compile_project_file(program_info: Program):
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

def run_project_file(in_file: str, program_info: Program):
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
    
    return output_object

def write_to_output_file(actual_out_file: str, output_object: subprocess.CompletedProcess):
    # write output to actual output files
    with open(actual_out_file, "w") as actfile:
        actual_lines = FileLines(output_object.stdout.splitlines(keepends=True))
        for line in actual_lines.raw:
            actfile.write(line)

def write_to_summary_file(sum_data: SummaryData):  # sourcery skip: ensure-file-closed
    # write summary of run information
        sumfile = open(sum_data.summary_out_file, "a")

        write_summary_header(sum_data.Header)

        write_summary_output(sum_data.output)

        if sum_data.expected_out_file == "":
            sum_data.i += 1
            sumfile.close()
            return

        write_summary_differences(sum_data.differences)

        write_summary_matching_data(sum_data.matching)

        sumfile.close()

def write_summary_header(sum_data: SummaryData) -> dict[str,]:
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

def write_summary_output(sum_data: SummaryData) -> dict[str,]:
    for line in sum_data.actual_lines.fancy:
        sum_data.sumfile.write(line)

def write_summary_differences(sum_data: SummaryData) -> dict[str,]:
    write_difference_header(sum_data)

    with open(sum_data.expected_out_file, "r") as efile:
        sum_data.expected_lines = FileLines(efile.readlines())

    write_line_differences(sum_data)

    write_extra_lines(sum_data)

def write_difference_header(sum_data: SummaryData):
    # write differences (if there were any)
    sum_data.isMismatched = 0

    sum_data.sumfile.write("---------------------------------------\n")
    sum_data.sumfile.write("Differences\n")
    sum_data.sumfile.write("---------------------------------------\n")

def write_line_differences(sum_data: SummaryData) -> None:
    if len(sum_data.actual_lines.split) != len(sum_data.expected_lines.split):
        sum_data.isMismatched = 1
        sum_data.sumfile.write(f"Difference in actual and expected output lengths:\n\t\tactual length:    {len(sum_data.actual_lines.split)}\n\t\texpected length:  {len(sum_data.expected_lines.split)}\n\n")

    # write line differences to summary out
    sum_data.sumfile.write("Mismatched lines:\n")
    for (aline, eline) in zip(sum_data.actual_lines.fancy, sum_data.expected_lines.fancy):
        if aline != eline:
            sum_data.mismatched_lines += 1
            sum_data.sumfile.write(f"\tactual:  \t{aline}\texpected:\t{eline}\n")

def write_extra_lines(sum_data: SummaryData):
    if sum_data.isMismatched != 1:
        return

    sum_data.extra_lines = len(sum_data.actual_lines.split) - len(sum_data.expected_lines.split)

    # actual is longer
    if len(sum_data.actual_lines.split) > len(sum_data.expected_lines.split): 
        write_extra_actual_lines(sum_data)

    # expected is longer
    else: 
        write_extra_expected_lines(sum_data)

def write_extra_actual_lines(sum_data: SummaryData):
    sum_data.max_lines = len(sum_data.actual_lines.split)
    sum_data.sumfile.write("Extra lines in actual_out:\n")

    start = len(sum_data.actual_lines.split) -sum_data.extra_lines
    stop = len(sum_data.actual_lines.split) # -1?
    for j in range(start, stop): 
        line = sum_data.actual_lines.fancy[j]
        sum_data.sumfile.write(f"\t\t\t\t{line}")
    
def write_extra_expected_lines(sum_data: SummaryData):
    sum_data.max_lines = len(sum_data.expected_lines.split)
    sum_data.extra_lines *= -1
    sum_data.sumfile.write("Extra lines in expected_out:\n")

    start = len(sum_data.expected_lines.split) -sum_data.extra_lines
    stop = len(sum_data.expected_lines.split) # -1?
    for j in range(start, stop): 
        line = sum_data.expected_lines.fancy[j]
        sum_data.sumfile.write(f"\t\t\t\t{line}")

def write_summary_matching_data(sum_data: SummaryData) -> dict[str,]:
    # write num of matching lines
    sum_data.mismatched_lines += sum_data.extra_lines
    sum_data.sumfile.write(f"\nMatching lines: ({sum_data.max_lines - sum_data.mismatched_lines}/{sum_data.max_lines})\n")
    sum_data.sumfile.write("-----------------------------------------\n")

def create_file_wrappers(in_file: str, environment: FileSystemInfo, sum_data: SummaryData, expected_out_files: list):
    sum_data.in_file = in_file
    sum_data.actual_out_file = os.path.join(environment.tests_dir, f"actual_out{sum_data.i}.txt")
    sum_data.expected_out_file = os.path.join(environment.tests_dir, f"expected_out{sum_data.i}.txt")

    # get expected_out_file if it exists
    if sum_data.expected_out_file not in expected_out_files:
        sum_data.expected_out_file = ""