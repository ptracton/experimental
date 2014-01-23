module top_level(
		 /*AUTOARG*/
		 // Inputs
		 clk, reset
		 );

   input clk;
   input reset;
   
   reg [7:0] flop;
   
   always @(posedge clk)
     if (reset)
       flop <= 8'b0;
     else
       flop <= flop + 8'h01;
      
endmodule // top_level
