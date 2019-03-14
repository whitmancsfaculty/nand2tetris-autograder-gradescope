// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/LocalsTest/LocalsTest.tst

load LocalsTest.asm,
output-file LocalsTest.out,
compare-to LocalsTest.cmp,
output-list RAM[0]%D1.6.1 RAM[300]%D1.6.1 RAM[301]%D1.6.1 RAM[302]%D1.6.1 
            RAM[303]%D1.6.1 RAM[304]%D1.6.1;

set RAM[0] 300,
set RAM[1] 300,
set RAM[300] 12,
set RAM[301] 34,
set RAM[302] 56,
set RAM[303] 78,
set RAM[304] 90,

repeat 300 {
  ticktock;
}

output;
