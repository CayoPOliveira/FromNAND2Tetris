/* módulo Mux4Way16 */

`ifndef _Mux4Way16_
`define _Mux4Way16_

`include "Mux16.v"

module Mux4Way16(out, a, b, c, d, sel);
    input[15:0] a,b,c, d;
    input [1:0] sel;
    output [15:0] out;
    wire [15:0] muxAB, muxCD;

    Mux16 mux0(muxAB, a, b, sel[0]);
    Mux16 mux1(muxCD, c, d, sel[0]);
    Mux16 mux2(out, muxAB, muxCD, sel[1]);

    // Descrição de conexões internas do módulo

endmodule

`endif
