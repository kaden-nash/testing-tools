import string

from src.TestRunner.file_search import file_search
from src.TestRunner.FileFoundOverload import FileFoundOverload
from src.TestRunner.FileSystemInfo import FileSystemInfo

MAX_RESULTS = 9

def get_path_from_user(env: FileSystemInfo):
    """
    Gets valid project file path

    Output:
        valid project file path
    """
    file = None
    valid_name_found = False
    while not valid_name_found:
        path = False or input("Enter name of file to test: ")
        potential_matches = file_search(env.cwd, path)

        try: 
            file = _isolate_file(potential_matches)

        except FileNotFoundError as e: 
            print(f"Error occurred: {e.args[0]}\n\n")
            path = _ask_user_again("Enter filename again or exit[C]: ")

        except FileFoundOverload as e: 
            print(f"Error occurred: {e.args[0]}\n\n")
            path = _ask_user_again("Enter filename again or exit[C] (you'll probably want to exit and switch to a different cwd): ")

        else:
            valid_name_found = True
            # print("Located file.")

    return file

def _ask_user_again(input_message: str) -> str:
    user_choice = input(input_message)
    if user_choice in "Cc":
        print("Exiting program.")
        exit(0)
    return user_choice

def _isolate_file(matches):
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
    elif len(matches) == MAX_RESULTS + 1:
        raise FileFoundOverload("9+ files were found matching. Please ensure you are in the right cwd.")
    else:
        correctIndex = _get_user_match_selection(matches) - 1
        match = matches[correctIndex]
    
    return match

def _get_user_match_selection(matches):
    """
    Takes user selection of correct file out of MAX_RESULTS possible found items.

    Input:
        list of matches

    Output: 
        index + 1 of place in list that has the right filepath
    """

    print("More than one file found.")

    for i, match in enumerate(matches):
        if i > MAX_RESULTS - 1:
            break

        print(f"[{i+1}] - {match}") 

    return _get_user_index()

def _get_user_index() -> int:
    isValid = False
    match_index = ""
    while not isValid:
        match_index = input("Please enter the number next to the correct file or enter C to cancel: ")

        invalid_input = any(ltr not in "Cc" and ltr not in string.digits for ltr in match_index)

        # exit if user cancelled
        if match_index in "Cc":
            exit(0)

        # try again
        if invalid_input:
            continue

        # check for numbers outside range
        if int(match_index) <= MAX_RESULTS + 1 and int(match_index) >= 1:
            isValid = True
    
    return int(match_index)