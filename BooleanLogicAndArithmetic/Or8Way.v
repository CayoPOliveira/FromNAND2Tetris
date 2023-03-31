/* módulo Or8Way */

`ifndef _Or8Way_
`define _Or8Way_

module Or8Way(out, a, b, c, d, e, f, g, h);
    input a,b,c,d,e,f,g,h;
    output out;

    wire orAB, orCD, orEF, orGH, orAB_CD, orEF_GH;
    or or0(orAB, a, b);
    or or1(orCD, c, d);
    or or2(orEF, e, f);
    or or3(orGH, g, h);
    or or4(orAB_CD, orAB, orCD);
    or or5(orEF_GH, orEF, orGH);
    or or6(out, orAB_CD, orEF_GH);

    // Descrição de conexões internas do módulo

endmodule

`endif
