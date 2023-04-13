/* módulo ProgramCounter */

`ifndef _ProgramCounter_
`define _ProgramCounter_

`include "Increment16.v"
`include "Mux16.v"
`include "Register16.v"

module ProgramCounter(out, in, load, inc, reset, clk);
    input load, inc, reset, clk;
    input [15:0] in;
    output [15:0] out;

    wire [15:0] Incrementado, outInc, outLoad, outReset, wireGround16;
    wire wireVcc;
    assign wireGround16 = 16'b0000000000000000;
    assign wireVcc = 1;

    //    Increment16    (  out,    in );
    Increment16 inc16(Incrementado, out);

    //      Mux16   (  out,      a,           b,            sel);
    Mux16 muxInc    (outInc,    out,        Incrementado,   inc);
    Mux16 muxLoad   (outLoad,   outInc,     in,             load);
    Mux16 muxReset  (outReset,  outLoad,    wireGround16,   reset);

    //   Register16 (out,   in,      load,   clk);
    Register16 reg16(out, outReset, wireVcc, clk);

    // Descrição de conexões internas do módulo

endmodule

`endif
