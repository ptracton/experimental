/*******************************************************************************
 
 Microblaze IO Bus, Bus Functional Model (bfm).
 
 This module contains tasks that can simulate a Microblaze IO Bus, bus master
 
********************************************************************************/
module mb_io_bfm_master (/*AUTOARG*/
			 // Outputs
			 IO_Addr_Strobe, IO_Read_Strobe, IO_Write_Strobe, IO_Address,
			 IO_Byte_Enable, IO_Write_Data,
			 // Inputs
			 clk, reset, IO_Ready, IO_Read_Data
			 ) ;

   input clk;
   input reset;
   output IO_Addr_Strobe;
   output IO_Read_Strobe;
   output IO_Write_Strobe;
   output [31:0] IO_Address;
   output [3:0]  IO_Byte_Enable;
   output [31:0] IO_Write_Data;
   input         IO_Ready;
   input [31:0]  IO_Read_Data;

   reg           IO_Addr_Strobe;
   reg           IO_Read_Strobe;
   reg           IO_Write_Strobe;
   reg [31:0] 	 IO_Address;
   reg [3:0] 	 IO_Byte_Enable;
   reg [31:0] 	 IO_Write_Data;

   //***************************************************************************
   //
   // This task will create a Microblaze IO Bus Write Cycle at the given
   // address, byte enables (which bytes to write) and data
   //
   //***************************************************************************
   task write;
      input [31:0] address;
      input [3:0]  byte_enable;      
      input [31:0] data;
      begin
	 $display("IO Write Addr: 0x%h  Data: 0x%h Enables 0x%h @ %d", address, data, byte_enable, $time);
	 
	 @(posedge clk);
	 IO_Addr_Strobe = 1;
	 IO_Address = address;
    	 IO_Write_Strobe = 1;	
    	 IO_Read_Strobe = 0;	            
	 IO_Byte_Enable = byte_enable;
	 case (byte_enable)
	   4'b1111 : IO_Write_Data = data;
	   4'b1100 : IO_Write_Data = {data[31:16], data[31:16]};
	   4'b0011 : IO_Write_Data = {data[15:00], data[15:00]};
	   4'b1000:  IO_Write_Data = {4{data[31:24]}};
	   4'b0100:  IO_Write_Data = {4{data[23:16]}};
	   4'b0010:  IO_Write_Data = {4{data[15:08]}};
	   4'b0001:  IO_Write_Data = {4{data[07:00]}};
	   default: IO_Write_Data = 32'hxxxx_xxxx;         
	 endcase // case (byte_enable)
	 

	 @(posedge IO_Ready);
	 IO_Addr_Strobe = 0;
	 IO_Address = 0;
	 
	 IO_Write_Data = 0;
	 IO_Write_Strobe = 0;
	 
	 IO_Byte_Enable = 4'h0;
	 
      end            
   endtask //
   

   //***************************************************************************
   //
   // This task will create a Microblaze IO Bus Read Cycle at the given
   // address, byte enables (which bytes to write) and data
   //
   //***************************************************************************   
   task read;
      input [31:0] address;
      input [3:0]  byte_enable;
      output [31:0] data;      
      begin
	 @(posedge clk);
	 IO_Addr_Strobe = 1;
	 IO_Address = address;
    	 IO_Read_Strobe = 1;
    	 IO_Write_Strobe = 0;		      
	 IO_Byte_Enable = byte_enable; 

	 @(posedge IO_Ready);
	 data = IO_Read_Data;
	 
	 IO_Addr_Strobe = 0;
	 IO_Address = 0;
	 
	 IO_Write_Data = 0;
	 IO_Write_Strobe = 0;
	 
	 IO_Byte_Enable = 4'h0;
	 $display("IO Read Addr: 0x%h  Data: 0x%h Enables 0x%h @ %d", address, data, byte_enable, $time);

      end
   endtask //
   
   
   
   
endmodule // mb_io_bfm_master
