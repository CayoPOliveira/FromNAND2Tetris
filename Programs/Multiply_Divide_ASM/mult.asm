// Estudante: Cayo Phellipe Ramalho de Oliveira
// Matricula: 12211ECP022

// Multiplica dois valores
// RAM[2] = RAM[0]*RAM[1]

// Descrição do Algoritmo
// 1  |#define B (Multiplier) as R0 (RAM [0])
// 2  |#define C (Multiplicand) as R1 (RAM [1])
// 3  |#define A (Product) as R2 (RAM[2]), as in A=B*C
// 4  |
// 5  |// main **********************
// 6  |if B == 0 or C == 0:
// 7  |   A = 0
// 8  |else
// 9  |   if B < 0 and C < 0 then
// 10 |       B = -B; C = -C
// 11 |       multiply ()
// 12 |       B = -B; C = -C
// 13 |   else
// 14 |       if B < 0 then
// 15 |           B = -B
// 16 |           multiply ()
// 17 |           B = -B; A = -A
// 18 |       else
// 19 |           if C < 0 then
// 20 |               C = -C
// 21 |               multiply ()
// 22 |               C = -C; A = -A
// 23 |           else
// 24 |               multiply ()
// 25 |           endif
// 26 |       endif
// 27 |   endif
// 28 |endif
// 29 |end
// 30 |
// 31 |// support ********************
// 32 |function multiply ():
// 33 |   i = B - 1; A = C
// 34 |   while i > 0 do
// 35 |       i = i - 1; A = A + C
// 36 |   endwhile
// 37 |endfunction

// Algoritmo ASM
(MULTIPLICA)
@R0       //if RAM[0]==0 go to IF_ZEROS
D=M
@IF_ZEROS
D;JEQ
@R1       //if RAM[1]==0 go to IF_ZEROS
D=M
@IF_ZEROS
D;JEQ
@ELSE_ZEROS
0;JMP
(IF_ZEROS) //RAM[2] = 0 (END)
  @R2
  M=0
  @ENDMULTIPLICA
  0;JMP
(ELSE_ZEROS) //if RAM[0] < 0 and RAM[1] < 0
  @R0
  D=M
  @RZNEG_AND_RUNEG
  D;JLT
  @ELSE_RZNEG_AND_RUNEG
  0;JMP
  (RZNEG_AND_RUNEG)
    @R1
    D=M
    @IF_RZNEG_AND_RUNEG
    D;JLT
    @ELSE_RZNEG_AND_RUNEG
    0;JMP
  (IF_RZNEG_AND_RUNEG) // M[0] < 0 AND M[1] < 0
    @R0    //M[j]= -M[0]
    D=-M
    @j
    M=D
    @R1    //M[k]= -M[1]
    D=-M
    @k
    M=D
    @j     //M[i] = M[j] - 1
    D=M-1
    @i
    M=D
    @k     //M[2] = M[k]
    D=M
    @R2
    M=D
    (WHILE3)  //while M[i] > 0 do
      @i
      D=M
      @ENDMULTIPLICA//endwhile if M[i]=0
      D;JEQ
      @R2     //M[2] = M[2] + M[k]
      D=M
      @k
      D=D+M
      @R2
      M=D
      @i      //M[i] = M[i] - 1;
      M=M-1
      @WHILE3
      0;JMP
  (ELSE_RZNEG_AND_RUNEG) //M[0] > 0 OR M[1] > 0
    @R0
    D=M
    @IF_RZNEG
    D;JLT
    @ELSE_RZNEG
    0;JMP
    (IF_RZNEG)  //if M[0] < 0
      @R0    //M[j]= -M[0]
      D=-M
      @j
      M=D
      @SKIPINVERTE //PULA A PROXIMA PARTE, É PARA INVERTER O VALOR NO FINAL
      0;JMP
      (INVERTE)
        @R2
        M=-M
        @ENDMULTIPLICA
        0;JMP
      (SKIPINVERTE)
      @j     //M[i] = M[j] - 1
      D=M-1
      @i
      M=D
      @R1     //M[2] = M[1]
      D=M
      @R2
      M=D
      (WHILE2)  //while M[i] > 0 do
        @i
        D=M
        @INVERTE//endwhile if M[i]=0
        D;JLE
        @R2     //M[2] = M[2] + M[1]
        D=M
        @R1
        D=D+M
        @R2
        M=D
        @i      //M[i] = M[i] - 1;
        M=M-1
        @WHILE2
        0;JMP
    (ELSE_RZNEG) //M[0] > 0
      @R1
      D=M
      @IF_RUNEG
      D;JLT
      @ELSE_RUNEG
      0;JMP
      (IF_RUNEG) //if M[1] < 0 (M[0] > 0)
        @R1    //M[j]= -M[1]
        D=-M
        @j
        M=D
        @R0    //M[i] = M[0] - 1
        D=M-1
        @i
        M=D
        @j     //M[2] = M[j]
        D=M
        @R2
        M=D
        (WHILE1)  //while M[i] > 0 do
          @i
          D=M
          @INVERTE//endwhile if M[i]=0
          D;JEQ
          @R2     //M[2] = M[2] + M[j]
          D=M
          @j
          D=D+M
          @R2
          M=D
          @i      //i = i - 1;
          M=M-1
          @WHILE1
          0;JMP
      (ELSE_RUNEG) //M[1] > 0 ( AND M[0] > 0)
        @R0     //i = M[0] - 1
        D=M-1
        @i
        M=D
        @R1     //M[2] = M[1]
        D=M
        @R2
        M=D
        (WHILE0)  //while M[i] > 0 do
          @i
          D=M
          @ENDMULTIPLICA//endwhile if M[i]=0
          D;JEQ
          @R2     //M[2] = M[2] + M[1]
          D=M
          @R1
          D=D+M
          @R2
          M=D
          @i      //M[i] = M[i] - 1;
          M=M-1
          @WHILE0
          0;JMP
(ENDMULTIPLICA)
@ENDMULTIPLICA
0;JMP