/* módulo FullAdder */

`ifndef _FullAdder_
`define _FullAdder_

`include "HalfAdder.v"

module FullAdder(s, cout, a, b, cin);
    input a, b, cin;
    output s, cout;
    wire sAB, cAB, cABC;

    HalfAdder ha0(sAB, cAB, a, b);
    HalfAdder ha1(s, cABC, sAB, cin);
    or o0(cout, cAB, cABC);


    // Descrição de conexões internas do módulo

endmodule

`endif
