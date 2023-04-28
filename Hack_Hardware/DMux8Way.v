/* módulo DMux8Way */

`ifndef _DMux8Way_
`define _DMux8Way_

`include "DMux.v"
`include "DMux4Way.v"

module DMux8Way(a, b, c, d, e, f, g, h, in, sel);
    input in;
    input [2:0] sel;
    output a, b, c, d, e, f, g, h;
    wire dmABCD, dmEFGH;

    DMux dm(dmABCD, dmEFGH, in, sel[2]);
    DMux4Way dm4w0(a,b,c,d, dmABCD, sel[1:0]);
    DMux4Way dm4w1(e,f,g,h, dmEFGH, sel[1:0]);


    // Descrição de conexões internas do módulo

endmodule

`endif
