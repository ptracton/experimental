`timescale 1ns/1ns

module testbench;


   reg clk;
   initial begin
      clk <= 1'b0;
      forever begin
         #10 clk <= ~clk;        
      end
   end

   reg reset;
   initial begin
      reset = 0;
      #100 reset = 1;
      #100 reset = 0;      
   end
   

   initial
     begin
        $display("Running Sim");        
     end
   
   initial begin
      #1000 $finish;      
   end

   top_level top(
		 .clk(clk),
		 .reset(reset)
		 );
   

   //
   // Dump signals for waveform viewing
   //
   dump dump();

   
endmodule // testbench
