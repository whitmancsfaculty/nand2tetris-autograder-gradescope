// Copyright Janet Davis, January 2018.
// Free for educational use.

// Tests the use of variables, or user-defined symbols, 
// through this somewhat creative infinite counting loop.

@foo
M=-1
@bar
M=1
@count
M=1
@count
M=M+1
@foo
D=M+1
D=D+1
@bar
D=D-M
@6
D;JEQ
