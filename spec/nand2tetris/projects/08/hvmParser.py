"""
hvmParser.py -- Parser class for Hack VM translator
Use advance to parse the next command; use getCommandType, getArg1, and getArg2 
to obtain the parsed components of that command.

Skeletonized by Janet Davis March 2016
Refactored by Janet Davis March 2019

You should not change any code in this Parser class.
"""

from hvmCommands import *

class Parser(object):
    def __init__(self, sourceName, comments=None):
        """
        Open 'sourceFile' and gets ready to parse it.
        """
        self.file = open(sourceName, 'r');
        self.lineNumber = 0
        self.line = ''
        self.rawline = ''
        self.comments = comments
        self.commandType = None
        self.arg1 = None
        self.arg2 = None

    def advance(self):
        """
        Reads the next command from the input and makes it the current command.
        Returns True if a command was found, False at end of file.
        """
        while True:
            if self.file:
                self.rawline = self.file.readline()
                if len(self.rawline) == 0:
                    return False
                self.rawline = self.rawline.replace('\n', '')
                self.line = self.rawline
                i = self.line.find('//')                
                if i != -1:
                    if self.comments:
                        self.comments.write('    '+self.line[i:]+'\n')
                    self.line = self.line[:i]
                self.line = self.line.replace('\t', ' ').strip()
                if len(self.line) == 0:
                    continue
                self._parse()
                return True
            else:
                return False

    def _parse(self):
        """
        Parses a VM command as command type and up to two argument valuess:
            command [arg1 [arg2]]
        """
        self.commandType = None
        self.arg1 = None
        self.arg2 = None
        self.comp = None
        self.jump = None
        self._parseCommandType()
        if self.commandType not in (C_ARITHMETIC, C_RETURN):
            self._parseArg1()
            if self.commandType in (C_PUSH, C_POP, C_FUNCTION, C_CALL):
                self._parseArg2()
                
        
    def _parseCommandType(self):
        """
        Parses the command type from a VM command, 
        storing the result in self.commandType.
        """
        # command is first run of non-whitespace
        self.line = self.line.lstrip()
        i = self.line.find(' ')
        if i != -1:
            command = self.line[:i]
            self.line = self.line[i:]
        else:
            command = self.line
            self.line = ''
        if len(command) == 0:
            return
        
        if command in T_ARITHMETIC:
            self.commandType = C_ARITHMETIC
            self.arg1 = command
        elif command == T_PUSH:
            self.commandType = C_PUSH
        elif command == T_POP:
            self.commandType = C_POP
        elif command == T_LABEL:
            self.commandType = C_LABEL
        elif command == T_GOTO:
            self.commandType = C_GOTO
        elif command == T_IF:
            self.commandType = C_IF
        elif command == T_FUNCTION:
            self.commandType = C_FUNCTION
        elif command == T_RETURN:
            self.commandType = C_RETURN
        elif command == T_CALL:
            self.commandType = C_CALL

    def getCommandType(self):
        """
        Returns the type of the current command:
            C_ARITHMETIC = 1
            C_PUSH = 2
            C_POP = 3
            C_LABEL = 4
            C_GOTO = 5
            C_IF = 6
            C_FUNCTION = 7
            C_RETURN = 8
            C_CALL = 9
        """
        return self.commandType

    def _parseArg(self):
        """
        Parses an argument, returning its value or None.
        """
        # arg is next run of non-whitespace
        self.line = self.line.lstrip()
        i = self.line.find(' ')
        if i != -1:
            arg = self.line[:i]
            self.line = self.line[i:]
        else:
            arg = self.line
            self.line = ''
        if len(arg) == 0:
            return None
        else:
            return arg
        
    def _parseArg1(self):
        """
        Parses an argument and stores it in self.arg1.
        """
        self.arg1 = self._parseArg()

    def _parseArg2(self):
        """
        Parses an argument and stores it in self.arg2.
        """
        self.arg2 = self._parseArg()

    def getArg1(self):
        """
        Returns the command's first argument (or None).
        """
        return self.arg1

    def getArg2(self):
        """
        Returns the command's second argument (or None).
        """
        return self.arg2

