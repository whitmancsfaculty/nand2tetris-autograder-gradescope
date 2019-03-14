// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/MemoryAccess/TempTest/TempTestVME.tst

load TempTest.vm,
output-file TempTest.out,
compare-to TempTest.cmp,
output-list RAM[256]%D1.6.1 RAM[257]%D1.6.1 RAM[5]%D1.6.1 RAM[11]%D1.6.1;

set sp 256,

repeat 6 {
  vmstep;
}

output;
