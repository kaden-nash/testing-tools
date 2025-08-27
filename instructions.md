Thanks for helping me test this testing kit!
Please let me know what you'd like to see improved upon.




Note that this file was formatted for VSCode and will look funny if you open with any other text editor.




What are these files?

	testCreator.exe and test.exe are testing tools that create test files and test your code with less human input.



Before doing anything with these files, note that it is assumed when you run them that you are in the current working directory (cwd) that contains your project file! Unexpected results will occur if this is not the case.

Creating test files with testCreator:

	What this program does:

			Looks at inputs you want to pass into a c file and the expected outputs the c file will give in a singular file, "tests_info.txt" that you will create. Then, it will separate the inputs and expected outputs into individual files ("in" files and "expected_out" files) which can then by analyzed by test.exe.


	1. Get the file path of "testCreator.exe". You will need the file path to run the file later. I recommend placing this file in the same folder as your c code as it simplifies the file path. 


	2. Manually create a text file called "tests_info.txt" in the same directory as the c file to be tested. This file will be read as the basis for corresponding test files: "in" files and "expected_out" files.

			Seriously, make sure this file is in the same directory as your c file! 
		
			In "tests_info.txt", you specify the input and output with the keywords "INPUT" and "OUTPUT".
				
					Pro tip: if something goes wrong you want to exit the execution of a program early, press "Ctrl" + "C" to cancel the execution.
			
			In the lines beneath the keywords, type the input and expected output respectively. 

					Since some inputs will not have expected outputs, the OUTPUT information for each INPUT is optional. In other words, you don't need to have the same amount of OUTPUT keywords as INPUT keywords.

			To represent blank lines, type "\n", not an empty line. 
				
					Also, there is no need to place newlines at the end of input/output lines that are not blank. Notice how in the sample, only lines I want blank have the newline character on them.

			Sample "tests_info.txt" file:
					INPUT
					type your input
					newline to follow
					\n
					there can be a blank line between INPUT and OUTPUT if you wish

					OUTPUT
					type
					\n
					the output like this
					\n



					INPUT
					there will be no output to follow



					INPUT
					something else
					OUTPUT
					I wouldn't leave lines under keywords blank, if I were you...



	3. Run "testCreator.exe" 

			Run with "./testCreator.exe" in bash or powershell if the file is in the same directory as the c program.

			Otherwise, run by typing in the file path to "testCreator.exe" on the command line and pressing enter(C:/something/like/this/testCreator.exe). You might do this if you want to store these files in a permanent location on your computer, like I do. 

			Ensure you run this program before running the next one!



Running c program through tests with test.exe:

	What this program does:

			After running your c program through the tests cases, it will aggregate all the outputs provided by each run of your c code and print them to a file created by the program, "summary_output.txt" found in the "tests" directory created by testCreator. Then, if OUTPUT was specified for a set of inputs, it will print the differences between the two files. 


	1. Run "test.exe"

			Run file with "./test.exe" in bash or powershell if the file is in the same directory as the c program.
			
					Otherwise, run by typing in the file path to "test.exe" on the command line and pressing enter(C:/something/like/this/test.exe).

			Note that there may be a small delay when running "test.exe".

			When running the executable, you will be prompted to enter the name of the file. 
			Enter the file name exactly as it appears in your file system. 



Running both commands at once:

	Ensure you run "testCreator.exe" before "test.exe" or else the testing will not work properly!

	Note that there may be a small delay when running "test.exe".

	1. On powershell:

			If in same directory as c file,

					./testCreator.exe; ./test.exe

			Otherwise,

					& "C:\path\to\testCreator.exe"; & "C:\path\to\test.exe"   

	2. On Bash or WSL:

			If in same directory as c file, 

					./testCreator.exe; ./test.exe

			Otherwise,
			
					/path/to/testCreator.exe; /path/to/test.exe