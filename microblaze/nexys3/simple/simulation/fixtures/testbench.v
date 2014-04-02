`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   13:12:52 03/26/2014
// Design Name:   top
// Module Name:   /home/ptracton/src/hardware/nexys3_testing/microblaze_simple/testbench.v
// Project Name:  microblaze_simple
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: top
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module testbench;

   // Inputs
   reg XCLK;
   reg XRESET;
   reg [31:0] XGPI;

   // Outputs
   wire       XREADY;
   wire [31:0] XGPO;
   
   // Instantiate the Unit Under Test (UUT)
   top uut (
            .XCLK(XCLK), 
            .XRESET(XRESET), 
            .XREADY(XREADY),
	    .XGPI(XGPI),
            .XGPO(XGPO)
            );

   initial begin
      XCLK = 0;
      forever
        #10 XCLK = ~XCLK;      
   end
   
   initial begin
      XRESET = 0;
      #12 XRESET = 1;
      #100 XRESET = 0;      
   end
   
   
   initial begin
      // Initialize Inputs
      XGPI = 32'b0;
      
      
      @(posedge XGPO != 32'b0);
      XGPI = 32'h12345678;
      
      #2000;
      	     
      // Add stimulus here
      $stop;          
   end
   dump dump0();
   
endmodule

