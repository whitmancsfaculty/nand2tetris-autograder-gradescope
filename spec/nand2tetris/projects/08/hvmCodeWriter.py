"""
hvmCodeWriter.py -- Code Writer class for Hack VM translator
"""

import os
from hvmCommands import *

# If debug is True, 
# then the VM code will be written as comments into the output ASM file.
debug = True

_segment_to_symbol = {"local":"LCL",
                      "argument":"ARG",
                      "this":"THIS",
                      "that":"THAT" }

class CodeWriter(object):

    def __init__(self, outputName):
        """
        Opens 'outputName' and gets ready to write it.
        """
        self.file = open(outputName, 'w')
        self.fileName = self.SetFileName(outputName)

        # used to generate unique labels
        self.labelNumber = 0

        # used to generate local labels
        self.functionName = None


    def Close(self):
        """
        Writes the terminal loop and closes the output file.
        """
        label = self._UniqueLabel()
        self._WriteCode('(%s), @%s, 0;JMP' % (label, label))
        self.file.close()


    def SetFileName(self, fileName):
        """
        Sets the current file name to 'fileName'.
        Restarts the local label counter.

        Strips the path and extension.  The resulting name must be a
        legal Hack Assembler identifier.
        """
        self.fileName = os.path.basename(fileName)
        self.fileName = os.path.splitext(self.fileName)[0]

    def Write(self, text):
        """ 
        Write directly to the file.
        """
        self.file.write(text)

    def _UniqueLabel(self):
        self.labelNumber += 1;
        return "label" + str(self.labelNumber)

    def _Static(self, index):
        return self.fileName + str(index)

    def _WriteCode(self, code):
        """
        Writes Hack assembly code to the output file.
        code should be a string containing ASM commands separated by commas,
        e.g., "@10, D=D+A, @0, M=D"
        """
        code = code.replace(',', '\n').replace(' ', '')
        self.Write(code + '\n')

    def _PushD(self):
        """
        Writes Hack assembly code to push the value from the D register 
        onto the stack.
        """
        self._WriteCode("@SP,A=M,M=D,@SP,M=M+1")

    def _PopD(self):
        """"
        Writes Hack assembly code to pop a value from the stack 
        into the D register.
        """
        self._WriteCode("@SP,AM=M-1,D=M")

    def _UnaryOp(self,op):
        """
        Writes Hack assembly code for a unary operator given as a string."
        """
        self._WriteCode("@SP,A=M-1,M=%sM" % (op))

    def _BinaryOp(self,op):
        """
        Writes Hack assembly code for a binary operator given as a string."
        """
        self._PopD()
        self._WriteCode("@SP,A=M-1,M=M%sD" % (op))

    def _ComparisonOp(self,op):
        """
        Writes Hack assembly code for a comparison operator given as a string."
        """
        label=self._UniqueLabel()
        self._PopD()
        self._WriteCode("@SP,A=M-1,D=M-D,M=-1")
        self._WriteCode("@%s,D;J%s" % (label, op))
        self._WriteCode("@SP,A=M-1,M=0")
        self._WriteCode("(%s)" % (label))

    def WriteArithmetic(self, command):
        """
        Writes Hack assembly code for the given command.
        TODO - Stage I - see Figure 7.5
        """
        if (debug):
            self.Write('    // %s\n' % command)
        if command == T_ADD:
            self._BinaryOp('+')
        elif command == T_SUB:
            self._BinaryOp('-')
        elif command == T_NEG:
            self._UnaryOp('-')
        elif command == T_EQ:
            self._ComparisonOp("EQ")
        elif command == T_GT:
            self._ComparisonOp("GT")
        elif command == T_LT:
            self._ComparisonOp("LT")
        elif command == T_AND:
            self._BinaryOp('&')
        elif command == T_OR:
            self._BinaryOp('|')
        elif command == T_NOT:
            self._UnaryOp('!')
        else:
            raise(ValueError, 'Bad arithmetic command')
        
    def _DirectMap(self, base, index):
        """
        Writes Hack assembly code to compute A = M[base] + index
        base should be a symbol "LCL" "ARG" "THIS" or "THAT"
        """
        self._WriteCode("@%s,D=M,@%d,A=A+D" % (base, int(index)))

    def _PushMem(self):
        """
        Writes Hack assembly code to push M[A] to the stack
        """
        self._WriteCode("D=M")
        self._PushD()

    def _PopMem(self):    
        """
        Writes Hack assembly code to pop the stack to M[A]
        """
        self._WriteCode("D=A,@R13,M=D") # Stash address in M[13]
        self._PopD()
        self._WriteCode("@R13,A=M,M=D")

    def WritePushPop(self, commandType, segment, index):
        """
        Write Hack code for 'commandType' (C_PUSH or C_POP).
        'segment' (string) is the segment name.
        'index' (int) is the offset in the segment.
        e.g., for the VM instruction "push constant 5",
        segment has the value "constant" and index has the value 5.
        TODO - Stage I & II - See Figure 7.6 and pp. 142-3
        """
        if commandType == C_PUSH:
            if (debug):
                self.Write('    // push %s %d\n' % (segment, int(index)))
            if segment == T_CONSTANT:
                self._WriteCode("@%d,D=A" % (int(index)))
                self._PushD()
            elif segment == T_STATIC:
                symbol = self._Static(index)
                self._WriteCode("@%s,D=M" % symbol)
                self._PushD()
            elif segment == T_POINTER:
                self._WriteCode("@%d" % (3+int(index)))
                self._PushMem()
            elif segment == T_TEMP:
                self._WriteCode("@%d" % (5+int(index)))
                self._PushMem()
            else: # argument, local, this, that
                self._DirectMap(_segment_to_symbol[segment], index)
                self._PushMem()
        elif commandType == C_POP:
            if (debug):
                self.Write('    // pop %s %d\n' % (segment, int(index)))
            if segment == T_STATIC:
                symbol = self._Static(index)
                self._PopD()
                self._WriteCode("@%s,M=D" % symbol)
            elif segment == T_POINTER:
                self._WriteCode("@%d" % (3+int(index)))
                self._PopMem()
            elif segment == T_TEMP:
                self._WriteCode("@%d" % (5+int(index)))
                self._PopMem()
            else: # argument, local, this, that
                self._DirectMap(_segment_to_symbol[segment], index)
                self._PopMem()
        else:
            raise(ValueError, 'Bad push/pop command')


    def WriteInit(self):
        """
        Writes assembly code that effects the VM initialization,
        also called bootstrap code. This code must be placed
        at the beginning of the output file.
        See p. 165, "Bootstrap Code"
        """
        if (debug):
            self.Write('    // Init\n')
        self._WriteCode("@256,D=A,@SP,M=D") # SP=256
        self.WriteCall("Sys.init", 0)       # Call Sys.init

    def _LocalLabel(self, label):
        if self.functionName:
            return self.functionName + "$" + label
        else:
            return self.fileName + "$$" + label

    def WriteLabel(self, label):
        """ 
        Writes assembly code that effects the label command.
        See section 8.2.1 and Figure 8.6.
        """
        if (debug):
            self.Write('    // label %s\n' % label)
        self._WriteCode("(%s)" % self._LocalLabel(label))

    def WriteGoto(self, label):
        """
        Writes assembly code that effects the goto command.
        See section 8.2.1 and Figure 8.6.
        """
        if (debug):
            self.Write('    // goto %s\n' % label)
        self._WriteCode("@%s, 0;JMP" % self._LocalLabel(label))

    def WriteIf(self,label):
        """
        Writes assembly code that effects the if-goto command.
        See section 8.2.1 and Figure 8.6.
        """
        if (debug):
            self.Write('    // if-goto %s\n' % label)
        self._PopD()
        self._WriteCode("@%s, D;JNE" % self._LocalLabel(label))

    def WriteCall(self, functionName, numArgs):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        """
        if (debug):
            self.Write('    // call %s %d\n' % (functionName, int(numArgs)))
        label = self._UniqueLabel()
        self._WriteCode("@%s, D=A" % label)
        self._PushD()
        self._WriteCode("@LCL, D=M")
        self._PushD()
        self._WriteCode("@ARG, D=M")
        self._PushD()
        self._WriteCode("@THIS, D=M")
        self._PushD()
        self._WriteCode("@THAT, D=M")
        self._PushD()
        self._WriteCode("@%d, D=A, @SP, D=M-D, @ARG, M=D" % (int(numArgs)+5))
        self._WriteCode("@SP, D=M, @LCL, M=D")
        self._WriteCode("@%s, 0;JMP" % functionName)
        self._WriteCode("(%s)" % label)

    def WriteReturn(self):
        """
        Writes assembly code that effects the return command.
        See Figure 8.5.
        """
        if (debug):
            self.Write('    // return\n')
        # FRAME = LCL       // FRAME is a temporary variable
        self._WriteCode("@LCL, D=M, @R14, M=D");
        # RET = *(FRAME-5)  // Put the return address in a temp var
        self._WriteCode("@5, D=A, @R14, A=M-D, D=M, @R15, M=D")
        # *ARG = pop()      // Reposition the return value for the caller
        self._PopD()
        self._WriteCode("@ARG, A=M, M=D")
        # SP = ARG+1        // Restore SP of caller
        self._WriteCode("@ARG, D=M+1, @SP, M=D")
        # THAT = *(FRAME-1) // Restore THAT of caller
        self._WriteCode("@R14, D=M, @1, A=D-A, D=M, @THAT, M=D")
        # THIS = *(FRAME-2) // Restore THIS of caller
        self._WriteCode("@R14, D=M, @2, A=D-A, D=M, @THIS, M=D")
        # ARG = *(FRAME-3)  // Restore ARG of caller
        self._WriteCode("@R14, D=M, @3, A=D-A, D=M, @ARG, M=D")
        # LCL = *(FRAME-4)  // Restore LCL of caller
        self._WriteCode("@R14, D=M, @4, A=D-A, D=M, @LCL, M=D")
        # goto RET         // Goto return address
        self._WriteCode("@R15, A=M, 0;JMP")


    def WriteFunction(self, functionName, numLocals):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        """
        if (debug):
            self.Write('    // function %s %d\n' % (functionName, int(numLocals)))
        self.functionName = functionName # For local labels
        self._WriteCode("(%s)" % functionName)
        for _ in range(int(numLocals)):      
             self._WriteCode("@0, D=A") 
             self._PushD()
