'''
Created on 11 Jul 2015

@author: matthew
'''

import sys
from lexer import *
from parser import *
import globaldecs as globals


if __name__ == '__main__':
    workingDirectory = sys.argv[1]
    inputFile = sys.argv[2]
    
    # step 1: use lexer to get list of time codes
    with open(inputFile, 'r') as texFile:
        tex = texFile.read()
    lexer.timecodeSet = set([])
    lexer.input(tex)
    
    for tok in lexer:
        print(tok)
        
    timecodeList = list(lexer.timecodeSet)
    timecodeList.sort()
    
    
    # step 2: iterate over timecode list, setting globals.currentTime, to produce
    #         series of .tex files.
    fileCounter = int(0)
    for time in timecodeList:
        currentTime = time
        print "+++++ " + str(currentTime)
        parser = yacc.yacc()
        parser.colourVariableCounter = int(0)
        parser.currentTime = time
        parser.isInTime = lambda x : (x.startTime <= currentTime and x.endTime > currentTime) 
        result = parser.parse(tex)
        filename = workingDirectory+"/part{num:04d}.tex".format(num=fileCounter)
        print filename
        with open(filename,"w") as outputFile:
            outputFile.write(result)
        fileCounter += 1
        
    
    