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
    // File name: projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm
    // Puts the first argument[0] elements of the Fibonacci series
    // in the memory, starting in the address given in argument[1].
    // Argument[0] and argument[1] are initialized by the test script 
    // before this code starts running.
    // push argument 1
@ARG
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
    // that = argument[1]
    // pop pointer 1
@4
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
    // push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
    // first element = 0
    // pop that 0
@THAT
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
    // push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
    // second element = 1
    // pop that 1
@THAT
D=M
@1
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
    // push constant 2
@2
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
    // num_of_elements -= 2 (first 2 elements are set)
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
    // label MAIN_LOOP_START
(FibonacciSeries$$MAIN_LOOP_START)
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
    // if num_of_elements > 0, goto COMPUTE_ELEMENT
    // if-goto COMPUTE_ELEMENT
@SP
AM=M-1
D=M
@FibonacciSeries$$COMPUTE_ELEMENT
D;JNE
    // otherwise, goto END_PROGRAM
    // goto END_PROGRAM
@FibonacciSeries$$END_PROGRAM
0;JMP
    // label COMPUTE_ELEMENT
(FibonacciSeries$$COMPUTE_ELEMENT)
    // push that 0
@THAT
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
    // push that 1
@THAT
D=M
@1
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
    // that[2] = that[0] + that[1]
    // pop that 2
@THAT
D=M
@2
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
    // push pointer 1
@4
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
    // add
@SP
AM=M-1
D=M
@SP
A=M-1
M=M+D
    // that += 1
    // pop pointer 1
@4
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
    // num_of_elements--
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
    // goto MAIN_LOOP_START
@FibonacciSeries$$MAIN_LOOP_START
0;JMP
    // label END_PROGRAM
(FibonacciSeries$$END_PROGRAM)
(label2)
@label2
0;JMP
