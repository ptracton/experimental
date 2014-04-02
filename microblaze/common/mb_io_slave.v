
module mb_io_slave (/*AUTOARG*/
		    // Outputs
		    IO_Read_Data, IO_Ready,
		    // Inputs
		    clk, reset, IO_Addr_Strobe, IO_Read_Strobe, IO_Write_Strobe,
		    IO_Address, IO_Byte_Enable, IO_Write_Data
		    ) ;


`define MB_IO_SLAVE_REG0 3'h0
`define MB_IO_SLAVE_REG1 3'h1
`define MB_IO_SLAVE_REG2 3'h2
`define MB_IO_SLAVE_REG3 3'h3
   
   input clk;
   input reset;
   input IO_Addr_Strobe;
   input IO_Read_Strobe;
   input IO_Write_Strobe;
   input [2:0] IO_Address;  
   input [3:0] 	IO_Byte_Enable;
   input [31:0] IO_Write_Data;   
   output [31:0] IO_Read_Data;
   output 	 IO_Ready;
   
   reg 		 read_ready;
   reg 		 write_ready;   
   reg [31:0] 	 IO_Read_Data;
   wire 	 IO_Ready;
   
   assign IO_Ready = read_ready | write_ready;
   
   always @(posedge clk)
     if (reset) begin
	write_ready <= 1'b0;	
     end
     else begin
	if (IO_Write_Strobe)
	  write_ready <= 1'b1;	
	else
	  write_ready <= 1'b0;
     end 

   //
   // Register 1
   //
   reg [0:31] reg0;   
   wire       reg0_decode = (IO_Address == `MB_IO_SLAVE_REG0);
   wire       reg0_write = reg0_decode &  IO_Write_Strobe;
   wire       reg0_read = reg0_decode & IO_Read_Strobe;
   
   always @(posedge clk)
     if (reset) begin
	reg0 <= 32'b0;
     end
     else begin
	if (reg0_write)
	  case (IO_Byte_Enable)
	    4'b1111: reg0 <= IO_Write_Data;
	    4'b1100: reg0[16:31] <= IO_Write_Data[31:16];
	    4'b0011: reg0[00:15] <= IO_Write_Data[15:00];
	    4'b1000: reg0[24:31] <= IO_Write_Data[31:24];
	    4'b0100: reg0[16:23] <= IO_Write_Data[23:16];
	    4'b0010: reg0[08:15] <= IO_Write_Data[15:08];
	    4'b0001: reg0[00:07] <= IO_Write_Data[07:00];
	    default: reg0 <= reg0;	    
	  endcase // case (byte_enable)	
     end // else: !if(reset)   

   
   //
   // Register 1
   //
   reg [0:31] reg1;   
   wire       reg1_decode = (IO_Address == `MB_IO_SLAVE_REG1);
   wire       reg1_write = reg1_decode &  IO_Write_Strobe;
   wire       reg1_read = reg1_decode & IO_Read_Strobe;
   
   always @(posedge clk)
     if (reset) begin
	reg1 <= 32'b0;
     end
     else begin
	if (reg1_write)
	  case (IO_Byte_Enable)
	    4'b1111: reg1 <= IO_Write_Data;
	    4'b1100: reg1[16:31] <= IO_Write_Data[31:16];
	    4'b0011: reg1[00:15] <= IO_Write_Data[15:00];
	    4'b1000: reg1[24:31] <= IO_Write_Data[31:24];
	    4'b0100: reg1[16:23] <= IO_Write_Data[23:16];
	    4'b0010: reg1[08:15] <= IO_Write_Data[15:08];
	    4'b0001: reg1[00:07] <= IO_Write_Data[07:00];
	    default: reg1 <= reg1;	    
	  endcase // case (byte_enable)	
     end // else: !if(reset)   

   //
   // Register 2
   //
   reg [0:31] reg2;   
   wire       reg2_decode = (IO_Address == `MB_IO_SLAVE_REG2);
   wire       reg2_write = reg2_decode &  IO_Write_Strobe;
   wire       reg2_read = reg2_decode & IO_Read_Strobe;
   
   always @(posedge clk)
     if (reset) begin
	reg2 <= 32'b0;
     end
     else begin
	if (reg2_write)
	  case (IO_Byte_Enable)
	    4'b1111: reg2 <= IO_Write_Data;
	    4'b1100: reg2[16:31] <= IO_Write_Data[31:16];
	    4'b0011: reg2[00:15] <= IO_Write_Data[15:00];
	    4'b1000: reg2[24:31] <= IO_Write_Data[31:24];
	    4'b0100: reg2[16:23] <= IO_Write_Data[23:16];
	    4'b0010: reg2[08:15] <= IO_Write_Data[15:08];
	    4'b0001: reg2[00:07] <= IO_Write_Data[07:00];
	    default: reg2 <= reg2;	    
	  endcase // case (byte_enable)	
     end // else: !if(reset)      

   //
   // Register 3
   //
   reg [0:31] reg3;   
   wire       reg3_decode = (IO_Address == `MB_IO_SLAVE_REG3);
   wire       reg3_write = reg3_decode &  IO_Write_Strobe;
   wire       reg3_read = reg3_decode & IO_Read_Strobe;
   
   always @(posedge clk)
     if (reset) begin
	reg3 <= 32'b0;
     end
     else begin
	if (reg3_write)
	  case (IO_Byte_Enable)
	    4'b1111: reg3 <= IO_Write_Data;
	    4'b1100: reg3[16:31] <= IO_Write_Data[31:16];
	    4'b0011: reg3[00:15] <= IO_Write_Data[15:00];
	    4'b1000: reg3[24:31] <= IO_Write_Data[31:24];
	    4'b0100: reg3[16:23] <= IO_Write_Data[23:16];
	    4'b0010: reg3[08:15] <= IO_Write_Data[15:08];
	    4'b0001: reg3[00:07] <= IO_Write_Data[07:00];
	    default: reg3 <= reg3;	    
	  endcase // case (byte_enable)	
     end // else: !if(reset)   
   
   
   //
   // Read Logic
   //

   always @(posedge clk)
     if (reset) begin
	IO_Read_Data <= 32'b0;
	read_ready <= 1'b0;	
     end
     else begin
	if (IO_Read_Strobe) begin
	   read_ready <= 1'b1;	
	   IO_Read_Data <= (reg0_read) ? reg0:
			   (reg1_read) ? reg1:
			   (reg2_read) ? reg2:
			   (reg3_read) ? reg3:
			   32'h0000_0000;

	end
	else begin
	   read_ready <= 1'b0;	
	end
     end
   
endmodule // mb_io_slave
