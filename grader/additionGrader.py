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

# def RunCode(inputLines, outputFilePath, codeFilePath):
#     outputFile = open(outputFilePath, 'a')
#     try:
#         out = subprocess.run('/usr/local/bin/python3 '+ codeFilePath, input=inputLines, stdout=outputFile, shell=True, timeout=1, stderr="/Users/benjaminhilton/gradertester/additionOutput.txt", text=True)
#     except subprocess.TimeoutExpired:
#         return 10
#     return out.returncode
    

x = "/Users/benjaminhilton/programming/pylearn/grader/additionInput.txt"
y = "/Users/benjaminhilton/programming/pylearn/grader/additionOutput.txt"
w = "/Users/benjaminhilton/programming/pylearn/grader/additionError.txt"
z = "addition.py"
# RunAllInput(x,y,z)
# print(RunCode(x,y,z))

def RunCode(codeFilePath, inputPath, outputPath, errorPath):
    inputFile = open(inputPath, 'r')
    outputFile = open(outputPath, 'a')
    errorFile = open(errorPath, 'a')
    try:
        out = subprocess.run('/usr/local/bin/python3 '+ codeFilePath, input=inputFile, stdout=outputFile, shell=True, timeout=1, stderr=errorFile, text=True)
    except subprocess.TimeoutExpired:
        return 10
    return out.returncode

# print(RunCode(z, x, y, w))
inputFile = open("additionInput.txt", 'r')
outputFile = open("additionOutput.txt", 'a')
# errorFile = open("add", 'a')
out = subprocess.run('/usr/local/bin/python3 addition.py', input=inputFile, stdout=outputFile, shell=True, timeout=1)
