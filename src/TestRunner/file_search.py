import os

def file_search(root_dir, searchTerm):
        """
        Searches for files containing a term in their filename.

        Input:
            root_dir: str - absolute directory path to begin searching through
            searchTerm: str - string term to search for in filenames

        Output:
            list of str - absolute paths of all files containing searchTerm in their names
        """
        matches = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
                for filename in filenames:
                    if searchTerm in filename:
                        full_path = os.path.join(dirpath, filename)
                        matches.append(full_path)

        return matches