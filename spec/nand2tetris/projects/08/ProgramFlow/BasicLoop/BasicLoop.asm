    // Init
@256
D=A
@SP
M=D
    // call Sys.init 0
@label1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(label1)
    // This file is part of www.nand2tetris.org
    // and the book "The Elements of Computing Systems"
    // by Nisan and Schocken, MIT Press.
    // File name: projects/08/ProgramFlow/BasicLoop/BasicLoop.vm
    // Computes the sum 1 + 2 + ... + argument[0] and pushes the 
    // result onto the stack. Argument[0] is initialized by the test 
    // script before this code starts running.
    // push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
    // initialize sum = 0
    // pop local 0
@LCL
D=M
@0
A=A+D
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
    // label LOOP_START
(BasicLoop$$LOOP_START)
    // push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
    // push local 0
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
    // add
@SP
AM=M-1
D=M
@SP
A=M-1
M=M+D
    // sum = sum + counter
    // pop local 0
@LCL
D=M
@0
A=A+D
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
    // push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
    // push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
    // sub
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
    // counter--
    // pop argument 0
@ARG
D=M
@0
A=A+D
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
    // push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
    // If counter > 0, goto LOOP_START
    // if-goto LOOP_START
@SP
AM=M-1
D=M
@BasicLoop$$LOOP_START
D;JNE
    // push local 0
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
(label2)
@label2
0;JMP
