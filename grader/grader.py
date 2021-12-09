import os
import subprocess

def RunCode(singleInputPath, singleOutputPath, resultPath, errorPath, codePath):
    sInputFile = open(singleInputPath, 'r')
    sOutputFile = open(singleOutputPath, 'a')
    resultFile = open(resultPath, 'a')
    errorFile = open(errorPath, 'a')
    errorFile.truncate(0)
    sOutputFile.truncate(0)
    try:
        out = subprocess.run('python3 '+codePath, shell=True, stdin=sInputFile, stdout=sOutputFile, stderr=errorFile, timeout=1)
        if out.returncode == 1:
            errorFile.close()
            errorFile = open(errorPath, 'r')
            for line in errorFile.readlines():
                print(line,file=resultFile,end='')
            print("NEWTESTCASE", file = resultFile, end ='\n')
        else:
            sOutputFile.close()
            sOutputFile = open(singleOutputPath, 'r')
            for line in sOutputFile.readlines():
                print(line,file=resultFile,end='')
            print("NEWTESTCASE", file = resultFile, end ='\n')
    except subprocess.TimeoutExpired:
        print("TIME LIMIT EXCEEDED",file=resultFile, end='\nNEWTESTCASE\n')
    sOutputFile.close()
    resultFile.close()
    errorFile.close()
    sInputFile.close()

def fileSplitter(fullInputPath, singleInputPath, singleOutputPath, resultPath, errorPath, codePath):
    singleInputFile = open(singleInputPath, 'a')
    singleInputFile.truncate(0)
    lines = open(fullInputPath, 'r').readlines()
    for line in lines:
        if line == '\n':
            singleInputFile.close()
            RunCode(singleInputPath, singleOutputPath, resultPath, errorPath, codePath)
            singleInputFile = open(singleInputPath, 'a')
            singleInputFile.truncate(0)
            continue
        print(line,file=singleInputFile, end='')
    singleInputFile.truncate(0)
    singleInputFile.close()

def CompareFiles():
    pass

fileSplitter('input.txt', 'singleInput.txt', 'singleOutput.txt', 'results.txt', 'singleError.txt', 'addition.py')