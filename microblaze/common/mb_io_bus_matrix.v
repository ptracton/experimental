
module mb_io_bus_matrix (/*AUTOARG*/
   // Outputs
   fault, M1_IO_Read_Data, M1_IO_Ready, M2_IO_Read_Data, M2_IO_Ready,
   S1_IO_Address, S1_IO_Addr_Strobe, S1_IO_Read_Strobe,
   S1_IO_Write_Strobe, S1_IO_Byte_Enable, S1_IO_Write_Data,
   S2_IO_Address, S2_IO_Addr_Strobe, S2_IO_Read_Strobe,
   S2_IO_Write_Strobe, S2_IO_Byte_Enable, S2_IO_Write_Data,
   S3_IO_Address, S3_IO_Addr_Strobe, S3_IO_Read_Strobe,
   S3_IO_Write_Strobe, S3_IO_Byte_Enable, S3_IO_Write_Data,
   S4_IO_Address, S4_IO_Addr_Strobe, S4_IO_Read_Strobe,
   S4_IO_Write_Strobe, S4_IO_Byte_Enable, S4_IO_Write_Data,
   // Inputs
   clk, reset, M1_Active, M1_IO_Address, M1_IO_Addr_Strobe,
   M1_IO_Read_Strobe, M1_IO_Write_Strobe, M1_IO_Byte_Enable,
   M1_IO_Write_Data, M2_Active, M2_IO_Address, M2_IO_Addr_Strobe,
   M2_IO_Read_Strobe, M2_IO_Write_Strobe, M2_IO_Byte_Enable,
   M2_IO_Write_Data, S1_IO_Read_Data, S1_IO_Ready, S2_IO_Read_Data,
   S2_IO_Ready, S3_IO_Read_Data, S3_IO_Ready, S4_IO_Read_Data,
   S4_IO_Ready
   ) ;

   parameter SLAVE1_START_ADDRESS = 32'hC000_0000;
   parameter SLAVE1_LENGTH        = 32'h0000_1000;    //4kbytes or 1Kword

   parameter SLAVE2_START_ADDRESS = 32'hC000_1000;
   parameter SLAVE2_LENGTH        = 32'h0000_1000;    //4kbytes or 1Kword
   
   parameter SLAVE3_START_ADDRESS = 32'hC000_2000;
   parameter SLAVE3_LENGTH        = 32'h0000_1000;    //4kbytes or 1Kword
   
   parameter SLAVE4_START_ADDRESS = 32'hC000_3000;
   parameter SLAVE4_LENGTH        = 32'h0000_1000;    //4kbytes or 1Kword
   
   //
   // System Interface
   //
   input clk;
   input reset;
   output fault;
   
   //
   // Master Interface
   //
   // This design can accept up to 2 masters
   //
   input  M1_Active;   
   input [31:0] M1_IO_Address;  
   input 	M1_IO_Addr_Strobe;
   input 	M1_IO_Read_Strobe;
   input 	M1_IO_Write_Strobe;   
   input [3:0] 	M1_IO_Byte_Enable;
   input [31:0] M1_IO_Write_Data;
   output [31:0] M1_IO_Read_Data;
   output        M1_IO_Ready;   

   input 	 M2_Active;   
   input [31:0]  M2_IO_Address;  
   input         M2_IO_Addr_Strobe;
   input         M2_IO_Read_Strobe;
   input         M2_IO_Write_Strobe;   
   input [3:0] 	 M2_IO_Byte_Enable;
   input [31:0]  M2_IO_Write_Data;
   output [31:0] M2_IO_Read_Data;
   output        M2_IO_Ready;      

   //
   // Slave Interface
   //
   output [31:0] S1_IO_Address;  
   output        S1_IO_Addr_Strobe;
   output        S1_IO_Read_Strobe;
   output        S1_IO_Write_Strobe;   
   output [3:0]  S1_IO_Byte_Enable;
   output [31:0] S1_IO_Write_Data;
   input [31:0]  S1_IO_Read_Data;
   input         S1_IO_Ready; 

   output [31:0] S2_IO_Address;  
   output        S2_IO_Addr_Strobe;
   output        S2_IO_Read_Strobe;
   output        S2_IO_Write_Strobe;   
   output [3:0]  S2_IO_Byte_Enable;
   output [31:0] S2_IO_Write_Data;
   input [31:0]  S2_IO_Read_Data;
   input         S2_IO_Ready; 

   output [31:0] S3_IO_Address;  
   output        S3_IO_Addr_Strobe;
   output        S3_IO_Read_Strobe;
   output        S3_IO_Write_Strobe;   
   output [3:0]  S3_IO_Byte_Enable;
   output [31:0] S3_IO_Write_Data;
   input [31:0]  S3_IO_Read_Data;
   input         S3_IO_Ready; 

   output [31:0] S4_IO_Address;  
   output        S4_IO_Addr_Strobe;
   output        S4_IO_Read_Strobe;
   output        S4_IO_Write_Strobe;   
   output [3:0]  S4_IO_Byte_Enable;
   output [31:0] S4_IO_Write_Data;
   input [31:0]  S4_IO_Read_Data;
   input         S4_IO_Ready;    


   //
   // Address range decode
   //
   wire 	 S1_Selected;
   wire 	 S2_Selected;
   wire 	 S3_Selected;
   wire 	 S4_Selected;

   assign S1_Selected = (M1_Active & (M1_IO_Address >= SLAVE1_START_ADDRESS) & 
			 (M1_IO_Address < SLAVE1_START_ADDRESS + SLAVE1_LENGTH)) || 
			(M2_Active & (M2_IO_Address >= SLAVE1_START_ADDRESS) & 
			 (M2_IO_Address < SLAVE1_START_ADDRESS + SLAVE1_LENGTH));
   
   assign S2_Selected = (M1_Active & (M1_IO_Address >= SLAVE2_START_ADDRESS) & 
			 (M1_IO_Address < SLAVE2_START_ADDRESS + SLAVE2_LENGTH)) || 
			(M2_Active & (M2_IO_Address >= SLAVE2_START_ADDRESS) & 
			 (M2_IO_Address < SLAVE2_START_ADDRESS + SLAVE2_LENGTH));
   
   assign S3_Selected = (M1_Active & (M1_IO_Address >= SLAVE3_START_ADDRESS) & 
			 (M1_IO_Address < SLAVE3_START_ADDRESS + SLAVE3_LENGTH)) || 
			(M2_Active & (M2_IO_Address >= SLAVE3_START_ADDRESS) & 
			 (M2_IO_Address < SLAVE3_START_ADDRESS + SLAVE3_LENGTH));
   
   assign S4_Selected = (M1_Active & (M1_IO_Address >= SLAVE4_START_ADDRESS) & 
			 (M1_IO_Address < SLAVE4_START_ADDRESS + SLAVE4_LENGTH)) || 
			(M2_Active & (M2_IO_Address >= SLAVE4_START_ADDRESS) & 
			 (M2_IO_Address < SLAVE4_START_ADDRESS + SLAVE4_LENGTH));
   

   //
   // Fault -- An invalid address is presented from a master.  
   //
   // Once asserted it can not be cleared!
   //
   reg 		 fault;
   always @(posedge clk)
     if (reset)
       fault <= 1'b0;
     else
       fault <= ((M1_Active | M2_Active)  & !S1_Selected & !S2_Selected & !S3_Selected & !S4_Selected) | fault;

   //
   // Master 1
   //
   assign M1_IO_Read_Data = (M1_Active & S1_Selected) ? S1_IO_Read_Data :
			    (M1_Active & S2_Selected) ? S2_IO_Read_Data :
			    (M1_Active & S3_Selected) ? S3_IO_Read_Data :
			    (M1_Active & S4_Selected) ? S4_IO_Read_Data : 32'h0000_0000;
  
   assign M1_IO_Ready = (M1_Active & S1_Selected) ? S1_IO_Ready :
			(M1_Active & S2_Selected) ? S2_IO_Ready :
			(M1_Active & S3_Selected) ? S3_IO_Ready :
			(M1_Active & S4_Selected) ? S4_IO_Ready : 1'b0;

   //
   // Master 2
   //
   assign M2_IO_Read_Data = (M2_Active & S1_Selected) ? S1_IO_Read_Data :
			    (M2_Active & S2_Selected) ? S2_IO_Read_Data :
			    (M2_Active & S3_Selected) ? S3_IO_Read_Data :
			    (M2_Active & S4_Selected) ? S4_IO_Read_Data : 32'h0000_0000;
   
   assign M2_IO_Ready = (M2_Active & S1_Selected) ? S1_IO_Ready :
			(M2_Active & S2_Selected) ? S2_IO_Ready :
			(M2_Active & S3_Selected) ? S3_IO_Ready :
			(M2_Active & S4_Selected) ? S4_IO_Ready : 1'b0;   
   
   //
   // Slave 1
   //
   assign S1_IO_Address = (S1_Selected & M1_Active) ? M1_IO_Address :
			  (S1_Selected & M2_Active) ? M2_IO_Address : 32'h0000_0000;
   
   assign S1_IO_Addr_Strobe = (S1_Selected & M1_Active) ? M1_IO_Addr_Strobe :
			      (S1_Selected & M2_Active) ? M2_IO_Addr_Strobe : 1'b0;

   assign S1_IO_Read_Strobe = (S1_Selected & M1_Active) ? M1_IO_Read_Strobe :
			      (S1_Selected & M2_Active) ? M2_IO_Read_Strobe : 1'b0;
   
   assign S1_IO_Write_Strobe = (S1_Selected & M1_Active) ? M1_IO_Write_Strobe :
			       (S1_Selected & M2_Active) ? M2_IO_Write_Strobe : 1'b0;
   
   assign S1_IO_Byte_Enable = (S1_Selected & M1_Active) ? M1_IO_Byte_Enable :
			      (S1_Selected & M2_Active) ? M2_IO_Byte_Enable : 4'b0;

   assign S1_IO_Write_Data = (S1_Selected & M1_Active) ? M1_IO_Write_Data :
			     (S1_Selected & M2_Active) ? M2_IO_Write_Data : 32'h0000_0000; 

   //
   // Slave 2
   //
   assign S2_IO_Address = (S2_Selected & M1_Active) ? M1_IO_Address :
			  (S2_Selected & M2_Active) ? M2_IO_Address : 32'h0000_0000;
   
   assign S2_IO_Addr_Strobe = (S2_Selected & M1_Active) ? M1_IO_Addr_Strobe :
			      (S2_Selected & M2_Active) ? M2_IO_Addr_Strobe : 1'b0;

   assign S2_IO_Read_Strobe = (S2_Selected & M1_Active) ? M1_IO_Read_Strobe :
			      (S2_Selected & M2_Active) ? M2_IO_Read_Strobe : 1'b0;
   
   assign S2_IO_Write_Strobe = (S2_Selected & M1_Active) ? M1_IO_Write_Strobe :
			       (S2_Selected & M2_Active) ? M2_IO_Write_Strobe : 1'b0;
   
   assign S2_IO_Byte_Enable = (S2_Selected & M1_Active) ? M1_IO_Byte_Enable :
			      (S2_Selected & M2_Active) ? M2_IO_Byte_Enable : 4'b0;

   assign S2_IO_Write_Data = (S2_Selected & M1_Active) ? M1_IO_Write_Data :
			     (S2_Selected & M2_Active) ? M2_IO_Write_Data : 32'h0000_0000;   
  
   //
   // Slave 3
   //
   
   assign S3_IO_Address = (S3_Selected & M1_Active) ? M1_IO_Address :
			  (S3_Selected & M2_Active) ? M2_IO_Address : 32'h0000_0000;
   
   assign S3_IO_Addr_Strobe = (S3_Selected & M1_Active) ? M1_IO_Addr_Strobe :
			      (S3_Selected & M2_Active) ? M2_IO_Addr_Strobe : 1'b0;

   assign S3_IO_Read_Strobe = (S3_Selected & M1_Active) ? M1_IO_Read_Strobe :
			      (S3_Selected & M2_Active) ? M2_IO_Read_Strobe : 1'b0;
   
   assign S3_IO_Write_Strobe = (S3_Selected & M1_Active) ? M1_IO_Write_Strobe :
			       (S3_Selected & M2_Active) ? M2_IO_Write_Strobe : 1'b0;
   
   assign S3_IO_Byte_Enable = (S3_Selected & M1_Active) ? M1_IO_Byte_Enable :
			      (S3_Selected & M2_Active) ? M2_IO_Byte_Enable : 4'b0;

   assign S3_IO_Write_Data = (S3_Selected & M1_Active) ? M1_IO_Write_Data :
			     (S3_Selected & M2_Active) ? M2_IO_Write_Data : 32'h0000_0000;   

   //
   // Slave 4
   //
   
   assign S4_IO_Address = (S4_Selected & M1_Active) ? M1_IO_Address :
			  (S4_Selected & M2_Active) ? M2_IO_Address : 32'h0000_0000;
   
   assign S4_IO_Addr_Strobe = (S4_Selected & M1_Active) ? M1_IO_Addr_Strobe :
			      (S4_Selected & M2_Active) ? M2_IO_Addr_Strobe : 1'b0;

   assign S4_IO_Read_Strobe = (S4_Selected & M1_Active) ? M1_IO_Read_Strobe :
			      (S4_Selected & M2_Active) ? M2_IO_Read_Strobe : 1'b0;
   
   assign S4_IO_Write_Strobe = (S4_Selected & M1_Active) ? M1_IO_Write_Strobe :
			       (S4_Selected & M2_Active) ? M2_IO_Write_Strobe : 1'b0;
   
   assign S4_IO_Byte_Enable = (S4_Selected & M1_Active) ? M1_IO_Byte_Enable :
			      (S4_Selected & M2_Active) ? M2_IO_Byte_Enable : 4'b0;

   assign S4_IO_Write_Data = (S4_Selected & M1_Active) ? M1_IO_Write_Data :
			     (S4_Selected & M2_Active) ? M2_IO_Write_Data : 32'h0000_0000;   
   
   
endmodule // mb_io_bus_matrix
