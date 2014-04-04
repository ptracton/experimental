`timescale 1ns / 1ns

module top(
           input 	 XCLK,
           input 	 XRESET,
           output 	 XREADY,
	   input [31:0]  XGPI,
           output [31:0] XGPO
           );


   //
   // System Clock and Reset Controller
   //
   wire 		 clk_user;           // Cleaned up and stable clock to the rest of the system
   wire 		 reset_user;         // Cleaned up and synchronous reset to the rest of the system 
   
   system_control sys_con(
			  .XCLK(XCLK),
			  .XRESET(XRESET),
			  .XREADY(XREADY),
			  .clk(clk_user),
			  .reset(reset_user)
			  );   
   //
   // IO BUS
   //
   wire 		 IO_Addr_Strobe;
   wire 		 IO_Read_Strobe;
   wire 		 IO_Write_Strobe;
   wire [31 : 0] 	 IO_Address;  
   wire [3 : 0] 	 IO_Byte_Enable;
   wire [31 : 0] 	 IO_Write_Data;   
   wire [31:0] 		 IO_Read_Data;
   wire 		 IO_Ready;
    
   //
   // Trace Signals
   //
   wire [0 : 31] 	 Trace_Instruction;
   wire [0:31] 		 Trace_PC;
   wire [0:4] 		 Trace_Reg_Addr;
   wire [0:14] 		 Trace_MSR_Reg;
   wire [0:31] 		 Trace_New_Reg_Value;
   wire [0 : 31] 	 Trace_Data_Address;
   wire [0 : 31] 	 Trace_Data_Write_Value;
   wire [0 : 3] 	 Trace_Data_Byte_Enable;

   wire 		 FIT1_Interrupt;
   wire 		 FIT1_Toggle;
   wire 		 PIT1_Interrupt;
   wire 		 PIT1_Toggle;
   
			 
   //
   // data2mem -p xc6slx16-csg324-3 -bm "ipcore_dir/microblaze_mcs_v1_4.bmm"  -bd ../software/applications/Debug/simple_application.elf   -bx . -u
   //
 
   
   //
   // Microblaze CPU
   //  
   microblaze_mcs_v1_4 mcs_0 (
                              .Clk(clk_user), // input Clk
                              .Reset(reset_user), // input Reset
                              .GPI1(XGPI), // input [31 : 0] GPI1
                              .GPO1(XGPO), // output [31 : 0] GPO1
			      .FIT1_Interrupt(FIT1_Interrupt), // output FIT1_Interrupt
			      .FIT1_Toggle(FIT1_Toggle), // output FIT1_Toggle
			      .PIT1_Interrupt(PIT1_Interrupt), // output PIT1_Interrupt
			      .PIT1_Toggle(PIT1_Toggle), // output PIT1_Toggle
			       			         
			      .IO_Addr_Strobe(IO_Addr_Strobe), // output IO_Addr_Strobe
			      .IO_Read_Strobe(IO_Read_Strobe), // output IO_Read_Strobe
			      .IO_Write_Strobe(IO_Write_Strobe), // output IO_Write_Strobe
			      .IO_Address(IO_Address), // output [31 : 0] IO_Address
			      .IO_Byte_Enable(IO_Byte_Enable), // output [3 : 0] IO_Byte_Enable
			      .IO_Write_Data(IO_Write_Data), // output [31 : 0] IO_Write_Data
			      .IO_Read_Data(IO_Read_Data), // input [31 : 0] IO_Read_Data
			      .IO_Ready(IO_Ready), // input IO_Ready
			      
                              .Trace_Instruction(Trace_Instruction), // output [0 : 31] Trace_Instruction
                              .Trace_Valid_Instr(Trace_Valid_Instr), // output Trace_Valid_Instr
                              .Trace_PC(Trace_PC), // output [0 : 31] Trace_PC
                              .Trace_Reg_Write(Trace_Reg_Write), // output Trace_Reg_Write
                              .Trace_Reg_Addr(Trace_Reg_Addr), // output [0 : 4] Trace_Reg_Addr
                              .Trace_MSR_Reg(Trace_MSR_Reg), // output [0 : 14] Trace_MSR_Reg
                              .Trace_New_Reg_Value(Trace_New_Reg_Value), // output [0 : 31] Trace_New_Reg_Value
                              .Trace_Jump_Taken(Trace_Jump_Taken), // output Trace_Jump_Taken
                              .Trace_Delay_Slot(Trace_Delay_Slot), // output Trace_Delay_Slot
                              .Trace_Data_Address(Trace_Data_Address), // output [0 : 31] Trace_Data_Address
                              .Trace_Data_Access(Trace_Data_Access), // output Trace_Data_Access
                              .Trace_Data_Read(Trace_Data_Read), // output Trace_Data_Read
                              .Trace_Data_Write(Trace_Data_Write), // output Trace_Data_Write
                              .Trace_Data_Write_Value(Trace_Data_Write_Value), // output [0 : 31] Trace_Data_Write_Value
                              .Trace_Data_Byte_Enable(Trace_Data_Byte_Enable), // output [0 : 3] Trace_Data_Byte_Enable
                              .Trace_MB_Halted(Trace_MB_Halted) // output Trace_MB_Halted
                              );
   //
   // Slave 2 -- Register testing module
   //
   mb_io_slave slave0(/*AUTOARG*/
		      // Outputs
		      .IO_Read_Data(IO_Read_Data), 
		      .IO_Ready(IO_Ready),
		      // Inputs
		      .clk(clk_user), 
		      .reset(reset_user), 
		      .IO_Addr_Strobe(IO_Addr_Strobe), 
		      .IO_Read_Strobe(IO_Read_Strobe), 
		      .IO_Write_Strobe(IO_Write_Strobe),
		      .IO_Address(IO_Address[4:2]), 
		      .IO_Byte_Enable(IO_Byte_Enable), 
		      .IO_Write_Data(IO_Write_Data)		    
		      ) ; 

  
endmodule // top

