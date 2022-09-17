// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// infinite loop
(INPUT)
@24576  // RAM[24576] is the designated keyboard memory
D=M     // take the keyboard input and store

@BLACKSET
D;JGT   // if the keyboard does something, D is not going to be 0.
        // if that's the case, jump to @screen

@WHITESET
0;JMP   // infinite loop waiting for keyboard input

(BLACKSET) // prepare for the blacken loop
@I      // set the index
M=0

(BLACK)
@I
D=M     // set I

@16384  // screen base address
A=A+D   // screen base address + I
M=-1    // set the black

@I
M=M+1   // increment I++

D=M     // set I to D in order to calculate

@8192
D=D-A   // I - end_address

@INPUT
D;JEQ   // if the I - end_address equal to 0, JMP to input

@BLACK
0;JMP

///////////////////////////////////////

(WHITESET)// prepare for the whiten loop
@I      // set the index
M=0

(WHITE)
@I
D=M     // set I

@16384  // screen base address
A=A+D   // screen base address + I
M=0    // set the white

@I
M=M+1   // increment I++

D=M     // set I to D in order to calculate

@8192
D=D-A   // I - end_address

@INPUT
D;JEQ   // if the I - end_address equal to 0, JMP to input

@WHITE
0;JMP