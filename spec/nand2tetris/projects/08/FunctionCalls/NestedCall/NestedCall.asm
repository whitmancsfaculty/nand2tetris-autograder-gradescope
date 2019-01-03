    // Init
    // Sys.vm for NestedCall test.
    //
    // Copyright (C) 2013 Mark A. Armbrust.
    // Permission granted for educational use.
    // Sys.init() calls Sys.main(), stores the return value in temp 1,
    //  and enters an infinite loop.
    // function Sys.init 0
(Sys.init)
    // call Sys.main 0
    // pop temp 1
@6
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
    // label LOOP
(Sys.init$LOOP)
    // goto LOOP
@Sys.init$LOOP
0;JMP
    // Sys.main() calls Sys.add12(123) and stores return value (135) in temp 0.
    // Returns 456.
    // function Sys.main 0
(Sys.main)
    // push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
    // call Sys.add12 1
    // pop temp 0
@5
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
    // push constant 246
@246
D=A
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
@R14
A=M
0;JMP
    // Sys.add12(int x) returns x+12.
    // It allocates 3 words of local storage to test the deallocation of local
    // storage during the return.
    // function Sys.add12 3
(Sys.add12)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
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
    // push constant 12
@12
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
@R14
A=M
0;JMP
(label1)
@label1
0;JMP
