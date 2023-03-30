/* módulo DMux4Way16 */

`ifndef _DMux4Way16_
`define _DMux4Way16_

`include "DMux16.v"

module DMux4Way16(a, b, c, d, in, sel);
    input [15:0] in;
    input [1:0] sel;
    output [15:0] a, b, c, d;

    wire [15:0] dmAB, dmCD;

    DMux16 dm160(dmAB, dmCD, in, sel[1]);
    DMux16 dm161(a, b, dmAB, sel[0]);
    DMux16 dm162(c, d, dmCD, sel[0]);

    // Descrição de conexões internas do módulo

endmodule

`endif
