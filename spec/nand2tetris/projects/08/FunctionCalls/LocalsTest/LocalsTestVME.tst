// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/LocalsTest/LocalsTestVME.tst

load LocalsTest.asm,
output-file LocalsTest.out,
compare-to LocalsTest.cmp,
output-list RAM[0]%D1.6.1 RAM[300]%D1.6.1 RAM[301]%D1.6.1 RAM[302]%D1.6.1 
            RAM[303]%D1.6.1 RAM[304]%D1.6.1;

set sp 300,
set local 300,

repeat 10 {
  vmstep;
}

output;
