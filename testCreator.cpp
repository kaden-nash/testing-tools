// NOTE: Compiling and Running
// g++ C:/Coding/testingtools/testCreator.cpp -o C:/Coding/testingtools/testCreator.exe
// C:/Coding/testingtools/testCreator.exe

// TODO: Add functionality to include a "Pass" statement in the tests_info file if the user want to make a comment or something 

#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>
#include <vector>
#include <exception>

using namespace std;
namespace fs = std::filesystem;

// creates the tests directory
fs::path createTestsDirectory(fs::path& currentPath) {
    // NOTE: add more directory names and /'s to create new direcotories. It will nest properly and without any extra work
    // create the directory.(don't if it already exists)
    fs::path newDirectoryPath = currentPath / "tests"; 
    fs::create_directory(newDirectoryPath);
    std::error_code ec;
    if (ec.value() != 0) {
        // cerr << "Error: " << ec.message() << " (Code: " << ec.value() << ")\n";
        cerr << "Directory \"tests\" creation/opening failed." << endl;
        exit(1);
    }
    return newDirectoryPath;
}

string readIOLines(ifstream& tests_infoFile, string& finalLine, string& line) {
    while(1) {
        getline(tests_infoFile, line);

        // handle blank lines
        if (line.empty()) { 
            if (tests_infoFile.eof()) 
                break; // if end of file is reached, exit loop

            continue; // continue consuming blank lines until "INPUT", "OUTPUT", or EOF is reached
        }

        if(line == "OUTPUT" || line == "INPUT")
            break;

        if(line.substr(0, 2) == "\\n") // handle newline inputs
            finalLine += "\n";
        else
            finalLine += line + "\n";

        if (tests_infoFile.eof()) // break out of loop if end of file
            break;
    }

    finalLine.erase(finalLine.size() - 1, 1); // consumes extra newline character
    return finalLine;
}

void writeIO(ofstream& file, fs::path& filePath, const string& line, const char& typeOfFile) {
    if (file.is_open()) {
        file << line;
        file.close();

        if (typeOfFile == 'i')
            cout << "Input sent to file: " << filePath << endl;
        else
            cout << "Output sent to file: " << filePath << endl;
    } else {
        if (typeOfFile == 'i')
            cerr << "Error sending input to file: " << filePath << endl;
        else
            cerr << "Error sending output to file: " << filePath << endl;
        exit(1);
    }
}

const int deleteExtraFile(const string& fileName, const fs::path& testsDirPath) {
    fs::path filePath = testsDirPath / fileName;
    int returnCode = 0;

        // remove file
        if (fs::exists(filePath)) {
            try {
                fs::remove(filePath);
            } catch (const exception& e) {
                cout << "Error occured trying to delete excess files: \n" << e.what() << endl;
            }
        } else 
            returnCode = 1; // file not found
        
    return returnCode;
}

int main () {
    // information to print to tests holders
    vector<string> inputs;
    vector<string> outputs;
    string line;
    string input;
    string output;
    int i = 0;
    int numInputs = 0;
    
    // get to current directory
    fs::path currentPath = fs::current_path();

    // find tests_info.txt in cwd
    fs::path inputFilePath = currentPath / "tests_info.txt";
    ifstream inputFile(inputFilePath);

    // create tests directory
    fs::path testsDirPath = createTestsDirectory(currentPath);

    if (inputFile.is_open()) {
        getline(inputFile, line); // get first line
        while (1) {
            if (inputFile.eof())
                break;

            if (line.empty()) {
                getline(inputFile, line); // get next line if blank
    
                if (inputFile.eof()) 
                    break; // if end of file is reached, exit loop

                continue; // continue consuming blank lines until "INPUT" or "OUTPUT" is reached
            }
            
            if (line == "INPUT") {
                // Read the inputs
                input = readIOLines(inputFile, input, line);
                inputs.push_back(input);
                input = "";

                // specify new input file information
                string inputFileName = "in" + to_string(i) + ".txt";
                fs::path inputFilePath = testsDirPath / inputFileName;
                ofstream inputFile(inputFilePath);

                // create input files
                writeIO(inputFile, inputFilePath, inputs[i], 'i');
                ++numInputs;
            }

            if (line == "OUTPUT") {
                // Read the second string
                output = readIOLines(inputFile, output, line);
                outputs.push_back(output);
                output = "";

                // specify new output file information
                string outputFileName = "expected_out" + to_string(i) + ".txt";
                fs::path outputFilePath = testsDirPath / outputFileName;
                ofstream outputFile(outputFilePath);

                // create new output file
                writeIO(outputFile, outputFilePath, outputs[i], 'o');
            } else {
                outputs.push_back(""); // add something to outputs to keep it on same i value
            }
  
            i++;
        }
    }
    else {
        cerr << "Couldn't open tests_info.txt\n\tDid you create it? \n\tIs in the cwd?" << endl;
        exit(1);
    }

    // delete extra files
    int holder = numInputs, success;
    string fileName;

    // delete extra in files
    while (1) {
        // specify new input file information
        fileName = "in" + to_string(numInputs) + ".txt";
        success = deleteExtraFile(fileName, testsDirPath); // delete file

        if (success != 0) // check whether this round of files exists
            break;

        ++numInputs;
    }

    // delete extra actual_out files
    numInputs = holder;
    while (1) {
        fileName = "actual_out" + to_string(numInputs) + ".txt";
        success = deleteExtraFile(fileName, testsDirPath);

        if (success != 0) // check whether this round of files exists
            break;

        ++numInputs;
    }

    // delete extra expected_out files
    numInputs = holder;
    while (1) {
        fileName = "expected_out" + to_string(numInputs) + ".txt";
        success = deleteExtraFile(fileName, testsDirPath);

        if (success != 0) // check whether this round of files exists
            break;

        ++numInputs;
    }

    return 0;
}