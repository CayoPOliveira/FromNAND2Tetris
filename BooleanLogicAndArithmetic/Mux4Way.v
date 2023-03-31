/* módulo Mux4Way */

`ifndef _Mux4Way_
`define _Mux4Way_

`include "Mux.v"

module Mux4Way(out, a, b, c, d, sel);
    input a,b,c,d;
    input [1:0] sel;
    output out;

    Mux mux0(muxAB, a, b, sel[0]);
    Mux mux1(muxCD, c, d, sel[0]);
    Mux mux2(out, muxAB, muxCD, sel[1]);

    // Descrição de conexões internas do módulo

endmodule

`endif
