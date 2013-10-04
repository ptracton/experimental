
module test1(
             clk,
             rst,

             in1,
             in2, in3,

             out1,
             out2, out3,

             bidir1
             );

  input wire clk;
  input wire rst;
  input wire in1, in2, in3;

  output out1;
  output wire out2;
  output reg out3;

  inout bidir1;
  

endmodule // test1
