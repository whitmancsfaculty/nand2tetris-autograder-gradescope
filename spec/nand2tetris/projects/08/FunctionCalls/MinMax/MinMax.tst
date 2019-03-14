// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/MinMax/MinMax.tst

// MinMax.asm is the result of translating both Main.vm and Sys.vm.

load MinMax.asm,
output-file MinMax.out,
compare-to MinMax.cmp,
output-list RAM[0]%D1.6.1 RAM[261]%D1.6.1;

repeat 6000 {
  ticktock;
}

output;
