
/* módulo DMux */

`ifndef _DMux_
`define _DMux_

`include "Mux.v"

module DMux(a, b, in, sel);

    input in, sel;
    output a, b;
    wire nsel;

    not notsel(nsel, sel);
    and andA(a, in, nsel);
    and andB(b, in, sel);

    // Descrição de conexões internas do módulo

endmodule

`endif
