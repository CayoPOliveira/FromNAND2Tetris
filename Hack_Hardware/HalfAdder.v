/* módulo HalfAdder */

`ifndef _HalfAdder_
`define _HalfAdder_

module HalfAdder(s, c, a, b);
    input a, b;
    output s, c;

    xor xor0(s, a, b);
    and and0(c, a, b);

    // Descrição de conexões internas do módulo

endmodule

`endif
