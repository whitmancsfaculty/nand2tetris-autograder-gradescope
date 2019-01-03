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
    // File name: projects/08/FunctionCalls/FibonacciElement/Main.vm
    // Computes the n'th element of the Fibonacci series, recursively.
    // n is given in argument[0].  Called by the Sys.init function 
    // (part of the Sys.vm file), which also pushes the argument[0] 
    // parameter before this code starts running.
    // function Main.fibonacci 0
(Main.fibonacci)
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
    // check if n < 2
    // lt
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
M=-1
@label2
D;JLT
@SP
A=M-1
M=0
(label2)
    // if-goto IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
    // goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
    // if n<2, return n
    // label IF_TRUE
(Main.fibonacci$IF_TRUE)
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
    // return
@LCL
D=M
@R14
M=D
@5
D=A
@R14
A=M-D
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R14
D=M
@1
A=D-A
D=M
@THAT
M=D
@R14
D=M
@2
A=D-A
D=M
@THIS
M=D
@R14
D=M
@3
A=D-A
D=M
@ARG
M=D
@R14
D=M
@4
A=D-A
D=M
@LCL
M=D
@R15
A=M
0;JMP
    // if n>=2, return fib(n-2)+fib(n-1)
    // label IF_FALSE
(Main.fibonacci$IF_FALSE)
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
    // compute fib(n-2)
    // call Main.fibonacci 1
@label3
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
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(label3)
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
    // compute fib(n-1)
    // call Main.fibonacci 1
@label4
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
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(label4)
    // return fib(n-1) + fib(n-2)
    // add
@SP
AM=M-1
D=M
@SP
A=M-1
M=M+D
    // return
@LCL
D=M
@R14
M=D
@5
D=A
@R14
A=M-D
D=M
@R15
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R14
D=M
@1
A=D-A
D=M
@THAT
M=D
@R14
D=M
@2
A=D-A
D=M
@THIS
M=D
@R14
D=M
@3
A=D-A
D=M
@ARG
M=D
@R14
D=M
@4
A=D-A
D=M
@LCL
M=D
@R15
A=M
0;JMP
    // This file is part of www.nand2tetris.org
    // and the book "The Elements of Computing Systems"
    // by Nisan and Schocken, MIT Press.
    // File name: projects/08/FunctionCalls/FibonacciElement/Sys.vm
    // Pushes n onto the stack and calls the Main.fibonacii function,
    // which computes the n'th element of the Fibonacci series.
    // The Sys.init function is called "automatically" by the 
    // bootstrap code.
    // function Sys.init 0
(Sys.init)
    // push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
    // Compute the 4'th fibonacci element
    // call Main.fibonacci 1
@label5
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
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(label5)
    // label WHILE
(Sys.init$WHILE)
    // Loop infinitely
    // goto WHILE
@Sys.init$WHILE
0;JMP
(label6)
@label6
0;JMP
