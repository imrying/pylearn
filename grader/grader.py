import os
import subprocess


# errorFile = open('additionError.txt', 'a')
def RunCode():
    inputFile = open('tempinput.txt', 'r')
    outputFile = open('additionOutput.txt', 'a')
    resultFile = open('result.txt', 'a')
    errorFile = open('additionError.txt', 'a')
    try:
        out = subprocess.run('python3 addition.py', shell=True, stdin=inputFile, stdout=outputFile, stderr=errorFile, timeout=1)
        print(out.returncode)
        print("STDERR ", out.stderr)
    except subprocess.TimeoutExpired:
        print("TIME LIMIT EXCEEDED",file=resultFile, end='\n')
        print()

def fileSplitter(inputPath, tempPath):
    tempFile = open(tempPath, 'a')
    lines = open(inputPath, 'r').readlines()
    for line in lines:
        if line == '\n':
            tempFile.close()
            #testcode
            tempFile = open(tempPath, 'a')
            tempFile.truncate(0)
            continue
        print(line,file=tempFile, end='')


fileSplitter('additionInput.txt', 'tempinput.txt')
