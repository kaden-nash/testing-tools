# FIXME: MAKE SURE YOU DON'T TURN THIS FILE INTO AN EXE WITHOUT MAKING A COPY!!
# FIXME: DO THIS
# FIXME: DON'T IGNORE TOP

import os

from src.TestRunner.ProjectFile import ProjectFile
from src.TestRunner.FileSystemInfo import FileSystemInfo
from src.TestRunner.TestFiles import TestFiles
from src.TestRunner.MainHelpers import *

def main():
    """
    Drives script
    """

    # program variables
    project_file = ProjectFile()
    program_info = project_file.type
    environment = FileSystemInfo()
    sum_data = SummaryData
    sum_data.summary_out_file = os.path.join(environment.tests_dir, "output_summary.txt")

    # testing variables
    if not os.path.exists(environment.tests_dir):
        create_test_files()

    in_files = TestFiles("in").files
    expected_out_files = TestFiles("expected_out").files

    compile_project_file(program_info)

    # clear previous data in output_summary.txt
    with open(sum_data.summary_out_file, "w"):
        pass

    # compare files
    for in_file in in_files:
        create_file_wrappers(in_file, environment, sum_data, expected_out_files)

        sum_data.output_object = run_project_file(sum_data)

        write_to_output_file(sum_data)

        write_to_summary_file(sum_data)

        sum_data.i += 1

    print("\nAll done! See output_summary.txt in the \"tests\" folder for the testing summary.")

if __name__ == "__main__":
    main()