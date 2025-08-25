import pytest
from unittest.mock import Mock, patch, mock_open, MagicMock
import os

from src.TestRunner.Main import main
from src.TestRunner.MainHelpers import SummaryData


@patch('src.TestRunner.Main.write_to_summary_file')
@patch('src.TestRunner.Main.write_to_output_file')
@patch('src.TestRunner.Main.run_program')
@patch('src.TestRunner.Main.create_file_wrappers')
@patch('src.TestRunner.Main.compile_program')
@patch('src.TestRunner.Main.TestFiles')
@patch('src.TestRunner.Main.create_test_files')
@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
@patch('src.TestRunner.Main.ProgramFactory')
@patch('src.TestRunner.Main.get_path_from_user')
@patch('src.TestRunner.Main.FileSystemInfo')
def test_main_successful_execution_with_existing_tests(
    mock_filesystem_info, mock_get_path, mock_program_factory, mock_file_open,
    mock_exists, mock_create_test_files, mock_test_files, mock_compile_program,
    mock_create_file_wrappers, mock_run_program, mock_write_to_output_file,
    mock_write_to_summary_file
):
    """Should successfully execute the complete testing workflow when all dependencies are available"""
    # Setup mocks
    mock_env = Mock()
    mock_env.tests_dir = "/test/dir"
    mock_filesystem_info.return_value = mock_env
    
    mock_get_path.return_value = "/path/to/program.java"
    
    mock_program = Mock()
    mock_factory = Mock()
    mock_factory.create_program.return_value = mock_program
    mock_program_factory.return_value = mock_factory
    
    mock_exists.return_value = True  # Tests directory exists
    
    mock_in_files = Mock()
    mock_in_files.files = ["in1.txt", "in2.txt"]
    mock_expected_files = Mock()
    mock_expected_files.files = ["expected_out1.txt", "expected_out2.txt"]
    
    mock_test_files.side_effect = [mock_in_files, mock_expected_files]
    
    mock_output_object = Mock()
    mock_run_program.return_value = mock_output_object
    
    # Execute
    main()
    
    # Verify workflow execution
    mock_filesystem_info.assert_called_once()
    mock_get_path.assert_called_once_with(mock_env)
    mock_program_factory.assert_called_once_with("/path/to/program.java")
    mock_factory.create_program.assert_called_once()
    mock_compile_program.assert_called_once_with(mock_program)
    
    # Verify test files processing
    assert mock_test_files.call_count == 2
    mock_test_files.assert_any_call("in")
    mock_test_files.assert_any_call("expected_out")
    
    # Verify file processing loop
    assert mock_create_file_wrappers.call_count == 2
    assert mock_run_program.call_count == 2
    assert mock_write_to_output_file.call_count == 2
    assert mock_write_to_summary_file.call_count == 2
    
    # Verify correct function call signatures
    mock_run_program.assert_any_call("in1.txt", mock_program)
    mock_run_program.assert_any_call("in2.txt", mock_program)


@patch('src.TestRunner.Main.write_to_summary_file')
@patch('src.TestRunner.Main.write_to_output_file')
@patch('src.TestRunner.Main.run_program')
@patch('src.TestRunner.Main.create_file_wrappers')
@patch('src.TestRunner.Main.compile_program')
@patch('src.TestRunner.Main.TestFiles')
@patch('src.TestRunner.Main.create_test_files')
@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
@patch('src.TestRunner.Main.ProgramFactory')
@patch('src.TestRunner.Main.get_path_from_user')
@patch('src.TestRunner.Main.FileSystemInfo')
def test_main_creates_test_files_when_directory_missing(
    mock_filesystem_info, mock_get_path, mock_program_factory, mock_file_open,
    mock_exists, mock_create_test_files, mock_test_files, mock_compile_program,
    mock_create_file_wrappers, mock_run_program, mock_write_to_output_file,
    mock_write_to_summary_file
):
    """Should handle missing test directory by creating test files via testCreator.exe"""
    # Setup mocks
    mock_env = Mock()
    mock_env.tests_dir = "/test/dir"
    mock_filesystem_info.return_value = mock_env
    
    mock_get_path.return_value = "/path/to/program.java"
    
    mock_program = Mock()
    mock_factory = Mock()
    mock_factory.create_program.return_value = mock_program
    mock_program_factory.return_value = mock_factory
    
    mock_exists.return_value = False  # Tests directory doesn't exist
    
    mock_in_files = Mock()
    mock_in_files.files = ["in1.txt"]
    mock_expected_files = Mock()
    mock_expected_files.files = ["expected_out1.txt"]
    
    mock_test_files.side_effect = [mock_in_files, mock_expected_files]
    
    mock_output_object = Mock()
    mock_run_program.return_value = mock_output_object
    
    # Execute
    main()
    
    # Verify test files creation was called
    mock_create_test_files.assert_called_once()
    
    # Verify rest of workflow still executes
    mock_compile_program.assert_called_once_with(mock_program)
    mock_run_program.assert_called_once()


@patch('src.TestRunner.Main.write_to_summary_file')
@patch('src.TestRunner.Main.write_to_output_file')
@patch('src.TestRunner.Main.run_program')
@patch('src.TestRunner.Main.create_file_wrappers')
@patch('src.TestRunner.Main.compile_program')
@patch('src.TestRunner.Main.TestFiles')
@patch('src.TestRunner.Main.create_test_files')
@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
@patch('src.TestRunner.Main.ProgramFactory')
@patch('src.TestRunner.Main.get_path_from_user')
@patch('src.TestRunner.Main.FileSystemInfo')
def test_main_initializes_summary_data_correctly(
    mock_filesystem_info, mock_get_path, mock_program_factory, mock_file_open,
    mock_exists, mock_create_test_files, mock_test_files, mock_compile_program,
    mock_create_file_wrappers, mock_run_program, mock_write_to_output_file,
    mock_write_to_summary_file
):
    """Should properly initialize SummaryData and set summary output file path"""
    # Setup mocks
    mock_env = Mock()
    mock_env.tests_dir = "/test/dir"
    mock_filesystem_info.return_value = mock_env
    
    mock_get_path.return_value = "/path/to/program.java"
    
    mock_program = Mock()
    mock_factory = Mock()
    mock_factory.create_program.return_value = mock_program
    mock_program_factory.return_value = mock_factory
    
    mock_exists.return_value = True
    
    mock_in_files = Mock()
    mock_in_files.files = ["in1.txt"]
    mock_expected_files = Mock()
    mock_expected_files.files = ["expected_out1.txt"]
    
    mock_test_files.side_effect = [mock_in_files, mock_expected_files]
    
    mock_output_object = Mock()
    mock_run_program.return_value = mock_output_object
    
    # Execute
    main()
    
    # Verify summary file path was set correctly
    expected_summary_path = os.path.join("/test/dir", "output_summary.txt")
    
    # Check that the summary file was opened for writing (clearing previous data)
    mock_file_open.assert_any_call(expected_summary_path, "w")


@patch('src.TestRunner.Main.compile_program')
@patch('src.TestRunner.Main.TestFiles')
@patch('src.TestRunner.Main.create_test_files')
@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
@patch('src.TestRunner.Main.ProgramFactory')
@patch('src.TestRunner.Main.get_path_from_user')
@patch('src.TestRunner.Main.FileSystemInfo')
def test_main_handles_compilation_failure(
    mock_filesystem_info, mock_get_path, mock_program_factory, mock_file_open,
    mock_exists, mock_create_test_files, mock_test_files, mock_compile_program
):
    """Should handle compilation failures gracefully and exit with appropriate error message"""
    # Setup mocks
    mock_env = Mock()
    mock_env.tests_dir = "/test/dir"
    mock_filesystem_info.return_value = mock_env
    
    mock_get_path.return_value = "/path/to/program.java"
    
    mock_program = Mock()
    mock_factory = Mock()
    mock_factory.create_program.return_value = mock_program
    mock_program_factory.return_value = mock_factory
    
    mock_exists.return_value = True
    
    mock_in_files = Mock()
    mock_in_files.files = ["in1.txt"]
    mock_expected_files = Mock()
    mock_expected_files.files = ["expected_out1.txt"]
    
    mock_test_files.side_effect = [mock_in_files, mock_expected_files]
    
    # Make compile_program raise SystemExit (simulating exit(0) call)
    mock_compile_program.side_effect = SystemExit(0)
    
    # Execute and verify SystemExit is raised
    with pytest.raises(SystemExit):
        main()
    
    # Verify compilation was attempted
    mock_compile_program.assert_called_once_with(mock_program)


@patch('src.TestRunner.Main.write_to_summary_file')
@patch('src.TestRunner.Main.write_to_output_file')
@patch('src.TestRunner.Main.run_program')
@patch('src.TestRunner.Main.create_file_wrappers')
@patch('src.TestRunner.Main.compile_program')
@patch('src.TestRunner.Main.TestFiles')
@patch('src.TestRunner.Main.create_test_files')
@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
@patch('src.TestRunner.Main.ProgramFactory')
@patch('src.TestRunner.Main.get_path_from_user')
@patch('src.TestRunner.Main.FileSystemInfo')
@patch('builtins.print')
def test_main_processes_multiple_test_files_and_generates_summary(
    mock_print, mock_filesystem_info, mock_get_path, mock_program_factory, mock_file_open,
    mock_exists, mock_create_test_files, mock_test_files, mock_compile_program,
    mock_create_file_wrappers, mock_run_program, mock_write_to_output_file,
    mock_write_to_summary_file
):
    """Should process multiple test files and generate comprehensive summary output"""
    # Setup mocks
    mock_env = Mock()
    mock_env.tests_dir = "/test/dir"
    mock_filesystem_info.return_value = mock_env
    
    mock_get_path.return_value = "/path/to/program.java"
    
    mock_program = Mock()
    mock_factory = Mock()
    mock_factory.create_program.return_value = mock_program
    mock_program_factory.return_value = mock_factory
    
    mock_exists.return_value = True
    
    # Multiple test files
    mock_in_files = Mock()
    mock_in_files.files = ["in1.txt", "in2.txt", "in3.txt"]
    mock_expected_files = Mock()
    mock_expected_files.files = ["expected_out1.txt", "expected_out2.txt", "expected_out3.txt"]
    
    mock_test_files.side_effect = [mock_in_files, mock_expected_files]
    
    mock_output_object = Mock()
    mock_run_program.return_value = mock_output_object
    
    # Execute
    main()
    
    # Verify all test files were processed
    assert mock_create_file_wrappers.call_count == 3
    assert mock_run_program.call_count == 3
    assert mock_write_to_output_file.call_count == 3
    assert mock_write_to_summary_file.call_count == 3
    
    # Verify completion message was printed
    mock_print.assert_any_call('\nAll done! See output_summary.txt in the "tests" folder for the testing summary.')