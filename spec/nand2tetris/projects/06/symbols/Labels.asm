// Copyright Janet Davis, January 2018.
// Free for educational use.

// Store the value 42 at memory location 17.
// This works only if the assembler properly counts instructions.

D=-1
(LABEL1)
@17
M=D
@LABEL3
D;JGE
D=0
@LABEL2
D;JEQ
@43
D=A
@17
M=D
@LABEL3
0;JMP
(LABEL2)
@42
D=A
@LABEL1
D;JGE
(LABEL3)
@LABEL3
0;JMP
