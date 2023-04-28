/* módulo And16 */

`ifndef _And16_
`define _And16_

module And16(out, a, b);
    input [15:0] a, b;
    output [15:0] out;

    and a0(out[0], a[0], b[0]);
    and a1(out[1], a[1], b[1]);
    and a2(out[2], a[2], b[2]);
    and a3(out[3], a[3], b[3]);
    and a4(out[4], a[4], b[4]);
    and a5(out[5], a[5], b[5]);
    and a6(out[6], a[6], b[6]);
    and a7(out[7], a[7], b[7]);
    and a8(out[8], a[8], b[8]);
    and a9(out[9], a[9], b[9]);
    and a10(out[10], a[10], b[10]);
    and a11(out[11], a[11], b[11]);
    and a12(out[12], a[12], b[12]);
    and a13(out[13], a[13], b[13]);
    and a14(out[14], a[14], b[14]);
    and a15(out[15], a[15], b[15]);

    // Descrição de conexões internas do módulo

endmodule

`endif
