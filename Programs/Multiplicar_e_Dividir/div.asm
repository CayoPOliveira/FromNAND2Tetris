// Estudante: Cayo Phellipe Ramalho de Oliveira
// Matricula: 12211ECP022

// Divide dois valores
// RAM[2] = RAM[0]/RAM[1]
// RAM[3] = RAM[0]%RAM[1]

// Descrição do Algoritmo
// 1  |#define N (Numerator) as R0 (RAM [0])
// 2  |#define D (Denominator) as R1 (RAM [1])
// 3  |#define Q (Quotient) as R2 (RAM [2])
// 4  |#define R (Rest) as R3 (RAM [3])
// 5  |
// 6  |// main **********************
// 7  |if R1 = 0 then
// 8  |   R2 := 0
// 9  |   R3 := 0x7FFF // or 32767, max. 16-bits positive integer
// 10 |else
// 11 |   if R0 = 0 then
// 12 |       R2 := 0; R3 := 0
// 13 |   else
// 14 |       divide ()
// 15 |   endif
// 16 |end
// 17 |
// 18 |// support ********************
// 19 |function divide ():
// 20 |   if R0 > 0 then
// 21 |       if R1 > 0 then
// 22 |           divide_unsigned()
// 23 |       else
// 24 |           R1 := -R1
// 25 |           divide_unsigned()
// 26 |           R1 := -R1; R2 := -R2
// 27 |       endif
// 28 |   else
// 29 |       if R1 > 0 then
// 30 |           R0 := -R0
// 31 |           divide_unsigned()
// 32 |           R0 := -R0
// 33 |           R2 := -R2
// 35 |           if R3 != 0 then
// 36 |               R2 := R2 - 1; R3 := R1 - R3
// 37 |           endif
// 38 |       else
// 39 |           R0 := -R0; R1 := -R1
// 40 |           divide_unsigned()
// 41 |           R0 := -R0; R1 := -R1; R2:= R2+1
// 42 |       endif
// 43 |   endif
// 44 |endfunction
// 45 |
// 46 |function divide_unsigned ():
// 47 |   R2 := 0; R3 := R0
// 48 |   while R3 >= R1 do
// 49 |       R2 := R2 + 1; R3 := R3 - R1
// 50 |   endwhile
// 51 |endfunction
// 52 |
(MAINDIVIDE)
  @16
  M=0
  @R1
  D=M
  @IF_DEN_ZERO // if R1 = 0
  D;JEQ

  @17
  M=0
  @R0
  D=M
  @IF_NUM_ZERO // if R0 = 0
  D;JEQ

  @R0
  D=M
  @IF_R0POS
  D;JGT
  @ELSE_R0POS
  0;JMP
  (IF_R0POS)//R0 positivo
    @18
    M=1
    @R1
    D=M
    @IF_R0POS_R1POS
    D;JGT
    @IF_R0POS_R1NEG
    0;JMP

    (IF_R0POS_R1POS)
      @19
      M=1
      @RETFUN_R0POS_R1POS //Chama a função divide_positivos
      D=A
      @return
      M=D
      @DIVIDE_POSITIVOS
      0;JMP
      (RETFUN_R0POS_R1POS)
    @END_MAINDIVIDE
    0;JMP
    (IF_R0POS_R1NEG)
      @20
      M=1
      @R1 // RAM[1] = -RAM[1]
      M=-M

      @RETFUN_R0POS_R1NEG //Chama a função divide_positivos
      D=A
      @return
      M=D
      @DIVIDE_POSITIVOS
      0;JMP
      (RETFUN_R0POS_R1NEG)

      @R1 // RAM[1] = -RAM[1]
      M=-M
      @R2 // RAM[2] = -RAM[2]
      M=-M

    @END_MAINDIVIDE
    0;JMP
  (ELSE_R0POS)//R0 negativo
    @21
    M=1
    @R1
    D=M
    @IF_R0NEG_R1POS
    D;JGT
    @IF_R0NEG_R1NEG
    0;JMP
    (IF_R0NEG_R1POS)
      @22
      M=1
      @R0 // RAM[0] = -RAM[0]
      M=-M

      @RETFUN_R0NEG_R1POS //Chama a função divide_positivos
      D=A
      @return
      M=D
      @DIVIDE_POSITIVOS
      0;JMP
      (RETFUN_R0NEG_R1POS)

      @R0 // RAM[0] = -RAM[0]
      M=-M
      @R2 // RAM[2] = -RAM[2]
      M=-M

      @R3
      D=M
      @IF_RESTODIFZERO
      D;JNE
      @END_RESTODIFZERO
      0;JMP
      (IF_RESTODIFZERO)
        @R2 //R2 := R2 - 1; R3 := R1 - R3
        M=M-1
        @R1
        D=M
        @R3
        M=D-M
      (END_RESTODIFZERO)
    @END_MAINDIVIDE
    0;JMP
    (IF_R0NEG_R1NEG)
      @23
      M=1
      @R0 // RAM[0] = -RAM[0] ; RAM[1] = -RAM[1]
      M=-M
      @R1
      M=-M

      @RETFUN_R0NEG_R1NEG //Chama a função divide_positivos
      D=A
      @return
      M=D
      @DIVIDE_POSITIVOS
      0;JMP
      (RETFUN_R0NEG_R1NEG)

      @R0 // RAM[0] = -RAM[0] ; RAM[1] = -RAM[1]; RAM[2] = RAM[2]+1
      M=-M
      @R1
      M=-M
      @R2
      M=M+1

(END_MAINDIVIDE)
  @END_MAINDIVIDE
  0;JMP

(IF_DEN_ZERO)
  @16
  M=1
  @R2
  M=0
  @32767
  D=A
  @R3
  M=D
@END_MAINDIVIDE
0;JMP

(IF_NUM_ZERO)
  @17
  M=1
  @R2
  M=0
  @R3
  M=0
@END_MAINDIVIDE
0;JMP

(DIVIDE_POSITIVOS)
  @R2 //RAM[2] = 0
  M=0
  @R0 //RAM[3] = RAM[0]
  D=M
  @R3
  M=D
  (WHILE)
    @R3
    D=M
    @R1
    D=D-M // D = R3 - R1
    @ENDWHILE // if R3 - R1 < 0 end -> !(R3 >= R1)
    D;JLT

    @R3 //R3 := R3 - R1
    M=D
    @R2 //R2 := R2 + 1
    M=M+1

    @WHILE
    0;JMP
  (ENDWHILE)
@return
A=M
0;JMP