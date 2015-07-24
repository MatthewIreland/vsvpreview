#!/usr/bin/python

'''
Created on 11 Jul 2015

@author: matthew
'''

import sys
import os
import subprocess
import datetime
from lexer import *
from parser import *
import globaldecs as globals
from FrameInput import *
import StringIO

class InvalidTmpFileError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    print "VSV Preview Script -- ALPHA RELEASE -- Expect bugs"
    #print "Make sure your LaTeX compiles as a standalone document before running this script!"
    
    #print sys.path[0]
    
    #workingDirectory = sys.argv[1]
    workingDirectory = "."
    try:
        scriptDir = sys.argv[1]
        inputFile = sys.argv[2]
        compileFrameDir = sys.argv[3]   # nasty hack. TODO remove.
        inputBase = (inputFile.split("/")[-1].split("."))[0]
    except IndexError:
        sys.stderr.write("Usage: processSrc.py <script dir> <input LaTeX file>.")
        sys.exit(1)
        
    scriptDir = scriptDir.rsplit('/', 1)[0]

    #print inputBase
    hdrDirectory = scriptDir+"/templates/"
    leftHdrFilename = hdrDirectory+"template_left_hdr.tex"
    rightHdrFilename = hdrDirectory+"template_right_hdr.tex"
    leftFooterFilename = hdrDirectory+"template_left_footer.tex"
    rightFooterFilename = hdrDirectory+"template_right_footer.tex"
    
    
    # step 0: check all requirements are accessible
    # TODO
    
    # step 1: strip comments and write output to intermediate file
    # TODO make this work from other directories
    dateString = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
    tmpDirectory = workingDirectory + "/" + dateString
    noCommentFile = tmpDirectory+"/nocomments.tex"
    if not os.path.exists(tmpDirectory):
        os.makedirs(tmpDirectory)
    subprocess.call(["./strip_comments.pl" + " " + inputFile+  " " +  noCommentFile], shell=True)
        
    # step 2: split up by frame and write each frame to a new intermediate file
    subprocess.call(["./split_frames.pl" + " " +  noCommentFile + " " + " " + tmpDirectory], shell=True)
    subprocess.call(["rm -f " + noCommentFile], shell=True)
    
    
    # step 3: read in each frame
    frameFiles = os.listdir(tmpDirectory)
    frameFiles.sort()
    frameList = []
    filePattern = re.compile("src_\d+_([\d\-:\.]+)_([\d\-:\.]+)_(left|right)\.tex")
    for frameFile in frameFiles:
        fileParts = filePattern.match(frameFile).groups()
        if (fileParts is None):
            raise InvalidTmpFileError(frameFile)
        frameStartTime = Timecode(fileParts[0])
        frameEndTime   = Timecode(fileParts[1])
        frameType      = fileParts[2]
        texSrc = None
        thisFrame  = None
        with open(tmpDirectory+"/"+frameFile, 'r') as f:
            texSrc = f.read()
        assert(texSrc is not None)
        if (frameType == "right"):
            thisFrame = RightFrameInput(texSrc,frameStartTime,frameEndTime)
        elif (frameType == "left"):
            thisFrame = LeftFrameInput(texSrc,frameStartTime,frameEndTime)
        else:
            raise UnknownFrameTypeError(frameType)
        assert (thisFrame is not None)
        frameList.append(thisFrame)
        
    # step 4: for each frame, create a pdf
    frameCounter=0
    for frame in frameList:
        # step 4.i: use lexer to get list of time codes
        # initialise lexer
        print "Parsing frame {fc:04d}".format(fc=frameCounter)
        #lexer = lex.lex(optimize=globals.MODE_DEBUG)
        lexer.timecodeSet = set([])
        lexer.largestSegment = 0
        lexer.startTimecode = frame.startTime
        lexer.endTimecode = frame.endTime
        lexer.input(frame.texSource)
        
        # TODO for some reason everything breaks without this
        for tok in lexer:
            #print(tok)
            pass
        
        frame.timecodeList = list(lexer.timecodeSet)
        if (not frame.startTime in frame.timecodeList):
            frame.timecodeList.append(frame.startTime)
        #frame.timecodeList.append(frame.endTime)
        frame.timecodeList.sort()
    
    
        # step 4.ii: iterate over timecode list, setting globals.currentTime, to produce
        #         series of .tex files.
        fileCounter = int(0)
        frameDirectory = tmpDirectory + "/{frameNum:04d}".format(frameNum=frameCounter)
        if (not os.path.exists(frameDirectory)):
            os.makedirs(frameDirectory)
        else:
            # TODO delete every tex file in the directory (with warning)
            pass   
        for time in frame.timecodeList:
            currentTime = time     # TODO get rid of this
            #print "+++++ " + str(currentTime)
            stderr = sys.stderr
            sys.stderr = StringIO.StringIO()
            parser = yacc.yacc(debug=0)
            sys.stderr = stderr
            parser.colourVariableCounter = int(0)
            parser.currentTime = time     # TODO get rid of this
            parser.isInTime = lambda x : (x.startTime <= currentTime and x.endTime > currentTime) 
            result = parser.parse(frame.texSource)
            filename = frameDirectory+"/part{fileNum:04d}.tex".format(fileNum=fileCounter)
            print filename
            with open(filename,"w") as outputFile:
                outputFile.write("% Generated by the VSV preview script on "+dateString+".\n\n")
                if isinstance(frame,LeftFrameInput):
                    outputFile.write("\input{meta/vsvhdr_left.tex}\n\n")
                elif isinstance(frame,RightFrameInput):
                    outputFile.write("\input{meta/vsvhdr_right.tex}\n\n")
                else:
                    raise UnknownFrameTypeError(frame)
                outputFile.write(result)
                outputFile.write("\input{meta/vsvftr.tex}\n")
            subprocess.call(["./remove_empty_lists.pl" + " " + filename], shell=True)   # TODO move this afterwards to speed things up
            fileCounter += 1
        frameCounter +=1

    # subprocess.call("rm -r "+tmpDirectory, shell=True)

    # step 5: compile all the sources and assemble a pdf
    print "Parsing done. Compiling frames to pdf."
    for frameCount in range(0,frameCounter):
        print " -- frame {fc:04d}".format(fc=frameCount)
        frame = frameList[frameCount]
        # TODO assert the file exists
        #commandString = "cd {fc:04d}; for f in *.tex; do pdflatex $f; done; pdftk *.pdf cat output "+inputBase+"_"+frame.type+"_{fc:04d}.pdf; cd ..".format(fc=frameCount)
        commandString = "./compile_frames.sh "+tmpDirectory+("/{fc:04d} ".format(fc=frameCount))+inputBase+"_"+frame.type+"_{fc:04d}.pdf ".format(fc=frameCount)+os.getcwd()
        #subprocess.call('cd '+'../test/0000; for f in *.tex; do pdflatex $f; done', stderr='/dev/null', shell=True)
        subprocess.call(commandString, shell=True)
        # TODO delete the tmp subdir
        
        
    #print "Done."

        
        
        
    
    