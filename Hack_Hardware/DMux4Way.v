/* módulo DMux4Way */

`ifndef _DMux4Way_
`define _DMux4Way_

`include "DMux.v"

module DMux4Way(a, b, c, d, in, sel);
    input in;
    input [1:0] sel;
    output a, b, c, d;

    wire dmAB, dmCD;

    DMux dm0(dmAB, dmCD, in, sel[1]);
    DMux dm1(a, b, dmAB, sel[0]);
    DMux dm2(c, d, dmCD, sel[0]);

    // Descrição de conexões internas do módulo

endmodule

`endif
