import os

from src.TestRunner.ProgramFactory import ProgramFactory
from src.TestRunner.get_path_from_user import get_path_from_user
from src.TestRunner.FileSystemInfo import FileSystemInfo
from src.TestRunner.TestFiles import TestFiles
from src.TestRunner.MainHelpers import *

def main():
    """
    Drives script
    """

    environment = FileSystemInfo()
    path = get_path_from_user(environment)
    program_factory = ProgramFactory(path)
    program = program_factory.create_program()

    sum_data = SummaryData
    sum_data.summary_out_file = os.path.join(environment.tests_dir, "output_summary.txt")

    if not os.path.exists(environment.tests_dir):
        create_test_files()

    in_files = TestFiles("in").files
    expected_out_files = TestFiles("expected_out").files

    compile_program(program)

    # clear previous data in output_summary.txt
    with open(sum_data.summary_out_file, "w"):
        pass

    for in_file in in_files:
        create_file_wrappers(in_file, environment, sum_data, expected_out_files)

        sum_data.output_object = run_program(sum_data)

        write_to_output_file(sum_data)

        write_to_summary_file(sum_data)

        sum_data.i += 1

    print("\nAll done! See output_summary.txt in the \"tests\" folder for the testing summary.")

if __name__ == "__main__":
    main()