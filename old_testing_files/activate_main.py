import sys
import os

# 1. Get the current script's directory (the 'testing' folder)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the project's root directory by going up one level
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

# 3. Insert the project root into Python's import path
sys.path.insert(0, project_root)

# Now, you can import Main from its correct location
from src.TestRunner.Main import main

if __name__ == "__main__":
    main()