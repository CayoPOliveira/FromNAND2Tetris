/* módulo Bit */

`ifndef _Bit_
`define _Bit_

`include "Mux.v"
`include "DLatch.v"

module Bit(out, in, load, clk);
    input in, load, clk;
    output out;
    wire w1;

    Mux mux(w1, out, in, load);
    DLatch dl(out, w1, clk);
    // Descrição de conexões internas do módulo

endmodule

`endif
