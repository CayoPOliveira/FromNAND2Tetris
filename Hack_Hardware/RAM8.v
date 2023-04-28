/* módulo RAM8 */

`ifndef _RAM8_
`define _RAM8_

`include "DMux8Way.v"
`include "Register16.v"
`include "Mux8Way16.v"

module RAM8(out, in, addr, write, clk);
    input [15:0] in;
    input [2:0] addr;
    input write, clk;
    output [15:0] out;

    wire wrt0, wrt1, wrt2, wrt3, wrt4, wrt5, wrt6, wrt7;
    wire [15:0] Out0, Out1, Out2, Out3, Out4, Out5, Out6, Out7;

    DMux8Way dmWriteAddr(wrt0, wrt1, wrt2, wrt3, wrt4, wrt5, wrt6, wrt7, write, addr);

    Register16 reg0(Out0, in, wrt0, clk);
    Register16 reg1(Out1, in, wrt1, clk);
    Register16 reg2(Out2, in, wrt2, clk);
    Register16 reg3(Out3, in, wrt3, clk);
    Register16 reg4(Out4, in, wrt4, clk);
    Register16 reg5(Out5, in, wrt5, clk);
    Register16 reg6(Out6, in, wrt6, clk);
    Register16 reg7(Out7, in, wrt7, clk);

    Mux8Way16 muxOut(out,Out0, Out1, Out2, Out3, Out4, Out5, Out6, Out7, addr);

    // Descrição de conexões internas do módulo

endmodule

`endif
