// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/fill/Fill.tst

load Fill.hack;
output-file Fill.out,
compare-to Fill.cmp,
output-list RAM[16385]%B1.16.1 RAM[16416]%B1.16.1 RAM[20480]%B1.16.1 RAM[24575]%B1.16.1;

// Unfortunately, we cannot press a key by setting the value of RAM[0x24576], 
// as the CPU emulator refreshes this value as part of its execution cycle.
//
// Experiments using expect were not a success, suggesting the CPU emulator
// does not use standard in for input.  A possible alternative, xdotool, 
// seems hard to learn and may not work on Gradescope's VMs as they probably 
// don't run Xwindows.
// 
// So we will test only the "no key pressed" behavior and leave the rest to 
// interactive testing as needed.

repeat 262144 {         // Repeat 32 times (instructions) per pixel on screen
  ticktock;
}
output;                 // All pixels should be white

repeat 262144 {         // Repeat 32 times (instructions) per pixel on screen
  ticktock;
}
output;                 // All pixels should be white
