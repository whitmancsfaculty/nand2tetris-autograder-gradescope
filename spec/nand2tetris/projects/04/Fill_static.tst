// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/fill/Fill_static.tst

load Fill_static.hack;
output-file Fill_static.out,
compare-to Fill_static.cmp,
output-list RAM[16385]%B1.16.1 RAM[16416]%B1.16.1 RAM[20480]%B1.16.1 RAM[24575]%B1.16.1;

repeat 32 {             // Repeat 32 times (instructions)
  ticktock;
}
output;                 // First pixel should be black

repeat 1024 {           // Repeat 32 times (instructions) per pixel in row
  ticktock;
}
output;                 // First pixel of second row should be black

repeat 262144 {         // Repeat 32 times (instructions) per pixel on screen
  ticktock;
}
output;                 // All pixels should be black

repeat 262144 {         // Repeat 32 times (instructions) per pixel on screen
  ticktock;
}
output;                 // All pixels should be black
