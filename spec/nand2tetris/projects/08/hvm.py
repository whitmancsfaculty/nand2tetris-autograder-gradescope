#!/usr/bin/python32
"""
hvm.py -- VM Translator
Skeletonized by Janet Davis March 2016
Refactored by Janet Davis March 2019

You should not change any code in this main program.
"""

import sys
import os
from hvmCommands import *
from hvmParser import *
from hvmCodeWriter import *

def process(sourceFile, codewriter):
    print('Processing ' + sourceFile)
    if debug:
        parser = Parser(sourceFile, codewriter)
    else:
        parser = Parser(sourceFile)
    codewriter.setFileName(sourceFile)
    
    while parser.advance():
        commandType = parser.getCommandType()
        if commandType == C_ARITHMETIC:
            codewriter.writeArithmetic(parser.getArg1())
        elif commandType in (C_PUSH, C_POP):
            codewriter.writePushPop(commandType, parser.getArg1(), 
                                                 int(parser.getArg2()))
        elif commandType == C_LABEL:
            codewriter.writeLabel(parser.getArg1())
        elif commandType == C_GOTO:
            codewriter.writeGoto(parser.getArg1())
        elif commandType == C_IF:
            codewriter.writeIf(parser.getArg1())
        elif commandType == C_FUNCTION:
            codewriter.writeFunction(parser.getArg1(), int(parser.getArg2()))
        elif commandType == C_RETURN:
            codewriter.writeReturn()
        elif commandType == C_CALL:
            codewriter.writeCall(parser.getArg1(), int(parser.getArg2()))


def usage():
    print('usage: hvm [options] sourceFile')
    print('    sourceFile may be a .vm file or a directory.')
    print('    If sourceFile is a directory, then all .vm files in')
    print('    the directory will be processed to a single sourceFile.asm')
    print()
    print('    -d option writes VM commands as comments in .asm file.')
    print('    -n option does not write Sys.init call in the bootstrap.')
    sys.exit(-1)
    

def main():
    sysinit = True
    while True:
        if len(sys.argv) >= 2:
            if sys.argv[1] == '-n':
                sysinit = False
                del (sys.argv[1])
                continue
            if sys.argv[1] == '-d':
                debug = True
                del (sys.argv[1])
                continue
        break
        
    if len(sys.argv) != 2:
        usage()
        
    sourceName = sys.argv[1]
    if os.path.isdir(sourceName):
        dirName = sourceName
    else:
        dirName = os.path.split(sourceName)[0]
    outName = os.path.split(sourceName)[-1]
    outName = os.path.splitext(outName)[0] + os.path.extsep + 'asm'
    if len(dirName) > 0:
        outName = dirName + os.path.sep + outName
    print('Creating file ' + outName)
    codewriter = CodeWriter(outName)
    if sysinit:
        codewriter.writeInit()
    
    if os.path.isdir(sourceName):
        # process all .vm files in dir
        dirName = sourceName
        print('Processing directory ' + dirName)
        for sourceName in os.listdir(dirName):
            if os.path.splitext(sourceName)[1].lower() == os.path.extsep + 'vm':
                process(dirName + os.path.sep + sourceName, codewriter)
    else:
        # process single .vm file
        process(sourceName, codewriter)

    codewriter.close()


main()
