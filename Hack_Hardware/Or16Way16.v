/* módulo Or16Way16 */

`ifndef _Or16Way16_
`define _Or16Way16_


module Or16Way16(out, in);
    input [15:0] in;
    output out;
    wire w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14;

    or or0(w1, in[0], in[1]);
    or or1(w2, in[2], in[3]);
    or or2(w3, in[4], in[5]);
    or or3(w4, in[6], in[7]);
    or or4(w5, in[8], in[9]);
    or or5(w6, in[10], in[11]);
    or or6(w7, in[12], in[13]);
    or or7(w8, in[14], in[15]);

    or or8(w9, w1, w2);
    or or9(w10, w3, w4);
    or or10(w11, w5, w6);
    or or11(w12, w7, w8);

    or or12(w13, w9, w10);
    or or13(w14, w11, w12);

    or or14(out, w13, w14);

    // Descrição de conexões internas do módulo

endmodule

`endif
