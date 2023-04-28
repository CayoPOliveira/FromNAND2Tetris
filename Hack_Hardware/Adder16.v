/* módulo Adder16 */

`ifndef _Adder16_
`define _Adder16_

`include "FullAdder.v"
`include "HalfAdder.v"

module Adder16(s, ovlf, a, b);
    input [15:0] a, b;
    output [15:0] s;
    output ovlf;

    HalfAdder ha(s[0], c0, a[0],b[0]);
    FullAdder fa1(s[1], c1, a[1], b[1], c0);
    FullAdder fa2(s[2], c2, a[2], b[2], c1);
    FullAdder fa3(s[3], c3, a[3], b[3], c2);
    FullAdder fa4(s[4], c4, a[4], b[4], c3);
    FullAdder fa5(s[5], c5, a[5], b[5], c4);
    FullAdder fa6(s[6], c6, a[6], b[6], c5);
    FullAdder fa7(s[7], c7, a[7], b[7], c6);
    FullAdder fa8(s[8], c8, a[8], b[8], c7);
    FullAdder fa9(s[9], c9, a[9], b[9], c8);
    FullAdder fa10(s[10], c10, a[10], b[10], c9);
    FullAdder fa11(s[11], c11, a[11], b[11], c10);
    FullAdder fa12(s[12], c12, a[12], b[12], c11);
    FullAdder fa13(s[13], c13, a[13], b[13], c12);
    FullAdder fa14(s[14], c14, a[14], b[14], c13);
    FullAdder fa15(s[15], ovlf, a[15], b[15], c14);



    // Descrição de conexões internas do módulo

endmodule

`endif
