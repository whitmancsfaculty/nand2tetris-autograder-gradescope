// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/ProgramFlow/BasicGoto/BasicGoto.tst

load BasicGoto.asm,
output-file BasicGoto.out,
compare-to BasicGoto.cmp,
output-list RAM[0]%D1.6.1 RAM[257]%D1.6.1;

set RAM[0] 256,

repeat 600 {
  ticktock;
}

output;
