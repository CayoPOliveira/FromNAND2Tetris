/* módulo Or16 */

`ifndef _Or16_
`define _Or16_

module Or16(out, a, b);
    input [15:0] a, b;
    output [15:0] out;

    or o0(out[0], a[0], b[0]);
    or o1(out[1], a[1], b[1]);
    or o2(out[2], a[2], b[2]);
    or o3(out[3], a[3], b[3]);
    or o4(out[4], a[4], b[4]);
    or o5(out[5], a[5], b[5]);
    or o6(out[6], a[6], b[6]);
    or o7(out[7], a[7], b[7]);
    or o8(out[8], a[8], b[8]);
    or o9(out[9], a[9], b[9]);
    or o10(out[10], a[10], b[10]);
    or o11(out[11], a[11], b[11]);
    or o12(out[12], a[12], b[12]);
    or o13(out[13], a[13], b[13]);
    or o14(out[14], a[14], b[14]);
    or o15(out[15], a[15], b[15]);

    // Descrição de conexões internas do módulo

endmodule

`endif
