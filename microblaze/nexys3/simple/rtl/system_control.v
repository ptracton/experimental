module system_control(
		      input  XCLK,
		      input  XRESET,
		      output XREADY,
		      output clk,
		      output reset
		      );
   
   reg [4:0] 		     reset_count;

   //
   // Input buffer to make sure the XCLK signal is routed
   // onto the low skew clock lines
   //
   wire 		     xclk_buf;
   IBUFG xclk_ibufg(.I(XCLK), .O(xclk_buf));

   //
   // Using our input clk buffer, we sample the input reset
   // signal.  if it is high, we hold the count to 1 (NOT 0!)
   // Once the input reset is released, we will count until
   // we wrap around to 0.  While this counter is not 0,
   // assert the reset signal to all other blocks.  This is done
   // to ensure we get a good clean synchronous reset of all flops
   // in the device
   //
   // This is the ONLY place we use xclk_buf or XRESET!
   //
   wire 		     LOCKED;
   //   assign dcm_reset = |reset_count;   
   assign reset = !LOCKED || (|reset_count);
   always @(posedge xclk_buf)
     if (XRESET)
       reset_count <= 'h01;
     else
       if ( (|reset_count) & XREADY)
         reset_count <= reset_count +1;

   //
   // DCM Reset Logic.  This is also off the xclk_buf since
   // we want this to be synchronous and held for a few clocks
   // in order for the DCM to get a good reset.  
   //
   // This is the ONLY place we use xclk_buf or XRESET!
   //
   reg [3:0] 		     dcm_reset_count;   
   assign dcm_reset = |dcm_reset_count;
   always @(posedge xclk_buf)
     if (XRESET)
       dcm_reset_count <= 'h01;
     else
       if (dcm_reset_count)
	 dcm_reset_count <= dcm_reset_count + 1;     
   
   //   
   // Clock buffer that ensures the clock going out to the hardware is on a low skew line
   //
   wire 		     dcm_clk_out;
   assign XREADY = LOCKED;   
   BUFG clk_bug (
		  .O(clk), // 1-bit output Clock buffer output
		  .I(dcm_clk_out) // 1-bit input Clock buffer input (S=0)
		  );

   //
   // DCM is the Digital Clock Manager.  It allows for a lot of different
   // features and functions
   //
   wire [7:0] 		     STATUS;   
   DCM_SP #(
	    .CLKDV_DIVIDE(2.0), // CLKDV divide value
	    // (1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,9,10,11,12,13,14,15,16).
	    .CLKFX_DIVIDE(1), // Divide value on CLKFX outputs - D - (1-32)
	    .CLKFX_MULTIPLY(4), // Multiply value on CLKFX outputs - M - (2-32)
	    .CLKIN_DIVIDE_BY_2("FALSE"), // CLKIN divide by two (TRUE/FALSE)
	    .CLKIN_PERIOD(10.0), // Input clock period specified in nS
	    .CLKOUT_PHASE_SHIFT("NONE"), // Output phase shift (NONE, FIXED, VARIABLE)
	    .CLK_FEEDBACK("1X"), // Feedback source (NONE, 1X, 2X)
	    .DESKEW_ADJUST("SYSTEM_SYNCHRONOUS"), // SYSTEM_SYNCHRNOUS or SOURCE_SYNCHRONOUS
	    .DFS_FREQUENCY_MODE("LOW"), // Unsupported - Do not change value
	    .DLL_FREQUENCY_MODE("LOW"), // Unsupported - Do not change value
	    .DSS_MODE("NONE"), // Unsupported - Do not change value
	    .DUTY_CYCLE_CORRECTION("TRUE"), // Unsupported - Do not change value
	    .FACTORY_JF(16'hc080), // Unsupported - Do not change value
	    .PHASE_SHIFT(0), // Amount of fixed phase shift (-255 to 255)
	    .STARTUP_WAIT("FALSE") // Delay config DONE until DCM_SP LOCKED (TRUE/FALSE)
	    )
   DCM_SP_inst (
		.CLK0(dcm_clk_out), // 1-bit output 0 degree clock output
		.CLK180(CLK180), // 1-bit output 180 degree clock output
		.CLK270(CLK270), // 1-bit output 270 degree clock output
		.CLK2X(CLK2X), // 1-bit output 2X clock frequency clock output
		.CLK2X180(CLK2X180), // 1-bit output 2X clock frequency, 180 degree clock output
		.CLK90(CLK90), // 1-bit output 90 degree clock output
		.CLKDV(CLKDV), // 1-bit output Divided clock output
		.CLKFX(CLKFX), // 1-bit output Digital Frequency Synthesizer output (DFS)
		.CLKFX180(CLKFX180), // 1-bit output 180 degree CLKFX output
		.LOCKED(LOCKED), // 1-bit output DCM_SP Lock Output
		.PSDONE(PSDONE), // 1-bit output Phase shift done output
		.STATUS(STATUS), // 8-bit output DCM_SP status output
		.CLKFB(clk), // 1-bit input Clock feedback input
		.CLKIN(xclk_buf), // 1-bit input Clock input
		.DSSEN(DSSEN), // 1-bit input Unsupported, specify to GND.
		.PSCLK(PSCLK), // 1-bit input Phase shift clock input
		.PSEN(PSEN), // 1-bit input Phase shift enable
		.PSINCDEC(PSINCDEC), // 1-bit input Phase shift increment/decrement input
		.RST(dcm_reset) // 1-bit input Active high reset input
		);
   
endmodule // system_control

/*
// Template

 system_control sys_con(
 .XCLK(),
 .XRESET(),
 .XREADY(),
 .clk(),
 .reset()
 );
*/
