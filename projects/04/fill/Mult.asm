(INIT)
@R3
M=0

@R2
M=0

(LOOP)
@R1
D=M

@R3
D=D-M

@END
D;JEQ

@R0
D=M

@R2
M=M+D

@R3
M=M+1

@LOOP
0;JMP

(END)
@END
0;JMP