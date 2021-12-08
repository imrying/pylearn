import os
import subprocess;

w = open('/Users/benjaminhilton/gradertester/additionError.txt', 'a')


def RunAllInput(inputFilePath, outputFilePath, codeFilePath):
    outputFile = open(outputFilePath, 'a')
    with open(inputFilePath) as f:
        lines = list(f)
        print("lines", lines)
        tempinput = ""
        for line in lines:
            if line == '\n':
                print("tempinput", tempinput)
                returncode = RunCode(tempinput,outputFilePath,codeFilePath)
                if returncode == 10:
                    print("TIME LIMIT EXCEEDED", file=outputFile)
                elif returncode == 1:
                    print("UNKNOWN ERROR OCCURED", file=outputFile)
                print("BREAK", file=outputFile)
            else:
                tempinput += line

def RunCode(inputLines, outputFilePath, codeFilePath):
    outputFile = open(outputFilePath, 'a')
    try:
        out = subprocess.run('/usr/local/bin/python3 '+ codeFilePath, input=inputLines, stdout=outputFile, shell=True, timeout=1, stderr=w, text=True)
    except subprocess.TimeoutExpired:
        return 10
    return out.returncode
    

x = "/Users/benjaminhilton/gradertester/additionInput.txt"
y = "/Users/benjaminhilton/gradertester/additionOutput.txt"
z = "addition.py"
RunAllInput(x,y,z)