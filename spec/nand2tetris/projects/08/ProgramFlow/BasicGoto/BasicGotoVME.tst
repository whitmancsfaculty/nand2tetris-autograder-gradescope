// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/ProgramFlow/BasicGoto/BasicGotoVME.tst

load BasicGoto.vm,
output-file BasicGoto.out,
compare-to BasicGoto.cmp,
output-list RAM[0]%D1.6.1 RAM[257]%D1.6.1;

set sp 256,

repeat 7 {
  vmstep;
}

output;
