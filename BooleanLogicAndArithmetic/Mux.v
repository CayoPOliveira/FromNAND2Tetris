/* módulo Mux */

`ifndef _Mux_
`define _Mux_

module Mux(out, a, b, sel);
    input a, b, sel;
    output out;
    wire w1, w2, nsel;


    nand na0(w1, sel, b);
    not notsel(nsel, sel);
    nand na1(w2, nsel, a);
    nand na2(out, w1, w2);

    // Descrição de conexões internas do módulo
    //  sel-------------|    |
    //                  |NAND|\w1
    //    b-------------|    | \|    |
    //                          |NAND|-----out
    //  sel--|NOT|-nsel-|    | /|    |
    //                  |NAND|/w2
    //    a-------------|    |


endmodule

`endif
