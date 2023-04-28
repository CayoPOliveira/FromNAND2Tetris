/* módulo ALU */

`ifndef _ALU_
`define _ALU_

`include "Mux16.v"
`include "Adder16.v"
`include "And16.v"
`include "Not16.v"
`include "Or16Way16.v"

module ALU(out, zr, ng, x, y, zx, nx, zy, ny, f, no);
    input [15:0] x, y;
    input zx, nx, zy, ny, f, no;
    output [15:0] out;
    output zr, ng;

    wire [15:0] wT, w1, not_w1, w2, w3, not_w3, w4, w5, w6, w7, not_w7;
    wire ovlf, not_zr;

    assign wT = 16'b0000000000000000;

    Mux16 muxZX(w1, x, wT, zx);
    Not16 notW1(not_w1, w1);
    Mux16 muxNX(w2, w1, not_w1, nx);

    Mux16 muxZY(w3, y, wT, zy);
    Not16 notW3(not_w3, w3);
    Mux16 muxNY(w4, w3, not_w3, ny);

    And16 andXY(w5, w2, w4);
    Adder16 addXY(w6, ovlf ,w2, w4);

    Mux16 muxF(w7, w5, w6, f);
    Not16 notW7(not_w7, w7);

    Mux16 muxNO(out, w7, not_w7, no);

    assign ng = out[15];

    Or16Way16 orNotZR(not_zr, out);
    not(zr, not_zr);





    // Descrição de conexões internas do módulo

endmodule

`endif
