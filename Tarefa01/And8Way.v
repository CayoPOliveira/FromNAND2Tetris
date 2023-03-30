/* módulo And8Way */

`ifndef _And8Way_
`define _And8Way_

module And8Way(out, a, b, c, d, e, f, g, h);
    input a,b,c,d,e,f,g,h;
    output out;

    wire andAB, andCD, andEF, andGH, andAB_CD, andEF_GH;
    and and0(andAB, a, b);
    and and1(andCD, c, d);
    and and2(andEF, e, f);
    and and3(andGH, g, h);
    and and4(andAB_CD, andAB, andCD);
    and and5(andEF_GH, andEF, andGH);
    and and6(out, andAB_CD, andEF_GH);

    // Descrição de conexões internas do módulo

endmodule

`endif
