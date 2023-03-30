/* módulo Mux8Way16 */

`ifndef _Mux8Way16_
`define _Mux8Way16_

`include "Mux4Way16.v"

module Mux8Way16(out, a, b, c, d, e, f, g, h, sel);
    input [15:0] a, b, c, d, e, f, g, h;
    input [2:0] sel;
    output [15:0] out;

    wire [15:0] muxABCD, muxEFGH;

    Mux4Way16 m4w160(muxABCD, a, b, c, d, sel[1:0]);
    Mux4Way16 m4w161(muxEFGH, e, f, g, h, sel[1:0]);
    Mux16 mux0(out, muxABCD, muxEFGH, sel[2]);

    // Descrição de conexões internas do módulo

endmodule

`endif
