/* módulo DLatch */

`ifndef _DLatch_
`define _DLatch_

module DLatch(q, d, clk);
    input d, clk;
    output q;

    wire notD, notCLK, notQ;
    wire w2,w3,w4,w5,w7,w8,w9;
    // Primeiro DFF
    not not1(notD, d);
    nand na1(w2, d, clk);
    nand na3(w4, notD, clk);
    nand na2(w5, w2, w3);
    nand na4(w3, w5, w4);
    // Segundo DFF
    not not2(notCLK, clk);
    not not3(notW5, w5);
    nand na5(w8, w5, notCLK);
    nand na7(w9, notCLK, notW5);
    nand na6(q, w8, notQ);
    nand na8(notQ, q, w9);

    // Descrição de conexões internas do módulo

endmodule

`endif
