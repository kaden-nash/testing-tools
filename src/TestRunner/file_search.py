import os
import subprocess

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