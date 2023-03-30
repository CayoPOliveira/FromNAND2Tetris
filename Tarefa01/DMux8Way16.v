/* módulo DMux8Way16 */

`ifndef _DMux8Way16_
`define _DMux8Way16_

`include "DMux16.v"
`include "DMux4Way16.v"

module DMux8Way16(a, b, c, d, e, f, g, h, in, sel);
    input [15:0] in;
    input [2:0] sel;
    output [15:0] a, b, c, d, e, f, g, h;
    wire [15:0] dmABCD, dmEFGH;

    DMux16 dm16(dmABCD, dmEFGH, in, sel[2]);
    DMux4Way16 dm4w160(a,b,c,d, dmABCD, sel[1:0]);
    DMux4Way16 dm4w161(e,f,g,h, dmEFGH, sel[1:0]);


    // Descrição de conexões internas do módulo

endmodule

`endif
