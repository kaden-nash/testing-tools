import os

from src.TestRunner.ProgramFactory import ProgramFactory
from src.TestRunner.get_path_from_user import get_path_from_user
from src.TestRunner.FileSystemInfo import FileSystemInfo
from src.TestRunner.MainHelpers import *

def main():
    """
    Drives the automated testing process for programs.
    
    Workflow:
    1. Get program file from user
    2. Create program object and test environment
    3. Compile program if needed
    4. Run tests against input files
    5. Compare outputs with expected results
    6. Generate summary report
    """

    # Setup environment and get program to test
    environment = FileSystemInfo()
    path = get_path_from_user(environment)
    program_factory = ProgramFactory(path)
    program = program_factory.create_program()

    sum_data = SummaryData()
    sum_data.summary_out_file = os.path.join(environment.tests_dir, "output_summary.txt")

    create_test_files(environment)

    in_files = file_search(environment.tests_dir, "in")
    expected_out_files = file_search(environment.tests_dir, "expected_out")

    if program.compilation_command != None:
        compile_program(program)

    # clear previous data in output_summary.txt
    with open(sum_data.summary_out_file, "w"):
        pass

    for in_file in in_files:
        create_file_wrappers(in_file, environment, sum_data, expected_out_files)

        sum_data.output_object = run_program(in_file, program)

        write_to_output_file(sum_data)

        write_to_summary_file(sum_data)

        sum_data.i += 1

    print("\nAll done! See output_summary.txt in the \"tests\" folder for the testing summary.")

if __name__ == "__main__":
    main()