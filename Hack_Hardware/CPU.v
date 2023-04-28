/* módulo CPU */

`ifndef _CPU_
`define _CPU_

`include "ProgramCounter.v"
`include "Register16.v"
`include "Mux16.v"
`include "ALU.v"

module CPU(pc, addrM, outM, writeM, instruct, inM, reset, clk);
    input [15:0] instruct, inM;
    input reset, clk;
    output [15:0] pc, addrM, outM;
    output writeM;

    //Instruct not
    wire wNotInst15;

    // 0 and 1
    wire wVCC, wGND;
    assign wVCC = 1;
    assign wGND = 0;

    //Registers outputs
    wire[15:0] REGa, REGd;
    //Registers input
    wire[15:0] wInputA;

    //ALU
    wire zr, ng;
    wire [15:0] outALU;
    wire [15:0] wYALU;

    //Jump Wires
    wire wNorALUflags, wandJ2, wandJ1, wandJ0, worJ01, wJ012, wJump;

    //Wires to load Registers
    wire wLoadD, wLoadA;

    //Output to Memory assigns the ALU output
    assign outM = outALU;

    //Write Memory Flag
    and andWriteM(writeM, instruct[15], instruct[3]);

    //Jump configs
    nor norZrNg(wNorALUflags, zr, ng);
    and andJ0(wandJ0, instruct[0], wNorALUflags);
    and andJ1(wandJ1, instruct[1], zr);
    and andJ2(wandJ2, instruct[2], ng);
    or orj01(worJ01, wandJ0, wandJ1);
    or orj012(wJ012, worJ01, wandJ2);
    and secJump(wJump, wJ012, instruct[15]);

    //ProgramCounter(out, in, load, inc, reset, clk)
    ProgramCounter PC(pc, REGa, wJump, wVCC, reset, clk);

    //Addres Memory
    assign addrM = REGa;

    //Load RegD
    and andLoadD(wLoadD, instruct[15], instruct[4]);
    Register16 D(REGd, outALU, wLoadD, clk);

    //Load RegA
    not NotInst15(wNotInst15, instruct[15]);
    Mux16 muxInstAC(wInputA, outALU, instruct, wNotInst15);
    or orLoadA(wLoadA, instruct[5], wNotInst15);
    Register16 A(REGa, wInputA, wLoadA, clk);

    //Use A or M
    Mux16 muxAM(wYALU, REGa, inM, instruct[12]);

    //ALU
    ALU alu(outALU, zr, ng, REGd, wYALU, instruct[11], instruct[10], instruct[9], instruct[8], instruct[7], instruct[6]);

endmodule

`endif
