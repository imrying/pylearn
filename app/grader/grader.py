import os
import sys
import subprocess

from app.models import Teacher

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
    print('resultpath', resultPath)
    resultFile = open(resultPath, 'a')
    resultFile.truncate(0)
    resultFile.close()
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

def CompareFiles(student_answer, correct_answer):
    torf = ""
    sys.stdin = open(student_answer, 'r')
    userResults = sys.stdin.read().split()
    sys.stdin = open(correct_answer, 'r')
    correctResults = sys.stdin.read().split()
    testcases = sum([x == 'NEWTESTCASE' for x in correctResults])
    userindex = 0
    correctindex = 0

    for _ in range(testcases):
        singleCorrectResult = []
        singleUserResult = []
        correct = True
        while (True):
            if (correctResults[correctindex] == 'NEWTESTCASE'):
                correctindex += 1
                break
            singleCorrectResult.append(correctResults[correctindex])
            correctindex += 1
        while True:
            if (userResults[userindex] == 'NEWTESTCASE'):
                userindex += 1
                break
            singleUserResult.append(userResults[userindex])
            userindex += 1
        if (len(singleUserResult) != len(singleCorrectResult)):
            correct = False
        else:
            for j in range(len(singleUserResult)):
                if (singleUserResult[j] != singleCorrectResult[j]):
                    correct = False
        torf += "t" if correct else "f"

    return torf



#fileSplitter('input.txt', 'singleInput.txt', 'singleOutput.txt', 'results.txt', 'singleError.txt', 'addition.py')
#print(CompareFiles(3))