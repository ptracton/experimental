//                              -*- Mode: Verilog -*-
// Filename        : uart_tasks.v
// Description     : UART Tasks
// Author          : Philip Tracton
// Created On      : Mon Apr 20 16:12:43 2015
// Last Modified By: Philip Tracton
// Last Modified On: Mon Apr 20 16:12:43 2015
// Update Count    : 0
// Status          : Unknown, Use with caution!


module uart_tasks;

   // general defines
`define mS *1000000
`define nS *1
`define uS *1000
`define Wait #
`define wait #
`define khz *1000

`define testbench testbench
`define test_failed `testbench.test_failed
`define UART_MASTER0      `testbench.uart_master0
`define UART_MASTER1      `testbench.uart_master1
`define UART_CLK          `testbench.clk_tb
`define UART_CONFIG uart_tasks.uart_config
`define UART_WRITE_CHAR uart_tasks.uart_write_char   
`define UART_READ_CHAR uart_tasks.uart_read_char
`define UART_READ_CHAR_NONASCII uart_tasks.uart_read_char_nonascii
`define UART_SET_MEMORY uart_tasks.uart_set_memory
`define UART_GET_MEMORY uart_tasks.uart_get_memory
`define UART_DUMP_MEMORY uart_tasks.uart_dump_memory
`define UART_RESET_IC    uart_tasks.uart_reset_ic
`define UART_PRESS_ENTER uart_tasks.uart_press_enter
`define UART_READ_ENTER uart_tasks.uart_read_enter

//
// Taken from http://asciitable.com/
//
`define LINE_FEED       8'h0A
`define CARRIAGE_RETURN 8'h0D
`define SPACE_CHAR      8'h20
`define NUMBER_0        8'h30
`define NUMBER_9        8'h39
`define LETTER_A        8'h41
`define LETTER_Z        8'h5A
`define LETTER_a        8'h61
`define LETTER_f        8'h66
`define LETTER_z        8'h7a

/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/
   task uart_config;
      begin
     
     $display("\033[93mTASK: UART Configure\033[0m");
     
     @(posedge `UART_CLK);
     //Turn on receive data interrupt
     `UART_MASTER0.wb_wr1(32'hFFFF0001,    4'h4, 32'h00010000); 
     
     @(posedge `UART_CLK);
     //FIFO Control, interrupt for each byte, clear fifos and enable
     `UART_MASTER0.wb_wr1(32'hFFFF0002,    4'h2, 32'h00000700);
     
     @(posedge `UART_CLK);
     //Line Control, enable writting to the baud rate registers
     `UART_MASTER0.wb_wr1(32'hFFFF0003,    4'h1, 32'h00000080);
     
     @(posedge `UART_CLK);
     //Baud Rate LSB
     `UART_MASTER0.wb_wr1(32'hFFFF0000,    4'h0, 32'h0000001A); //115200bps from 50 MHz
     
     @(posedge `UART_CLK);
     //Baud Rate MSB
     `UART_MASTER0.wb_wr1(32'hFFFF0001,    4'h4, 32'h00000000);          
     
     @(posedge `UART_CLK);
     //Line Control, 8 bits data, 1 stop bit, no parity
     `UART_MASTER0.wb_wr1(32'hFFFF0003,    4'h1, 32'h00000003);  
      end
   endtask // uart_config


/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/
   task uart_write_char;
      input [7:0] char;
      begin
     @(posedge `UART_CLK);
     `UART_MASTER0.wb_wr1(32'hFFFF0000,    4'h0, {24'h000000, char});
     $display("TASK: UART Write = %c @ %d", char, $time);
     @(posedge testbench.uart0_int);
     @(posedge `UART_CLK);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     if (testbench.read_word != char)
       `UART_MASTER0.wb_wr1(32'hFFFF0002,    4'h2, 32'h00000700);
       begin
          $display("FAIL: UART Write = 0x%h NOT 0x%h @ %d", testbench.read_word[7:0], char, $time); 
          `test_failed <= 1;                             
       end
     `wait(1`mS);   
      end      
   endtask // uart_write_char
   
/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/
   task uart_read_char;
      input [7:0] expected;
      begin
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("\033[93mTASK: UART Read = %c @ %d", testbench.read_word, $time);
     if (testbench.read_word != expected)
       begin
          $display("\033[1;31mFAIL: UART Read = 0x%h NOT 0x%h @ %d\033[0m", testbench.read_word[7:0], expected, $time);            
          `test_failed <= 1;            
       end 
      end
   endtask // uart_read_char

/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/
   function [7:0] convert_to_ascii;
      input [7:0] src;
      if ((src >= 8'h0) && (src <= 8'h9))
    convert_to_ascii = src + 8'h30;      
      else 
    convert_to_ascii = src + 8'h57;
   endfunction // convert_to_ascii


/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/
   task uart_press_enter;      
      begin
      @(posedge `UART_CLK);
     $display("TASK: UART Press Enter @ %d", $time);
     `UART_MASTER0.wb_wr1(32'hFFFF0000,    4'h0, {24'h000000, `CARRIAGE_RETURN});

     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
//   if (testbench.read_word[7:0] != `CARRIAGE_RETURN)
//     $display("TASK: UART Press Enter 0x0A= 0x%h @ %d", testbench.read_word, $time);

     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
//   if (testbench.read_word[7:0] != `CARRIAGE_RETURN)
//     $display("TASK: UART Press Enter 0x0D= 0x%h @ %d", testbench.read_word, $time);
     
      end      
   endtask // uart_press_enter   

/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/
   task uart_read_enter;      
      begin
     $display("READ Enter before command prompt");   
     `UART_READ_CHAR(`CARRIAGE_RETURN);
     `UART_READ_CHAR(`LINE_FEED);
      end      
   endtask // uart_press_enter

/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/
   task uart_read_char_nonascii;
      input [7:0] expected;
      begin
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("TASK: UART Read = 0x%h @ %d", testbench.read_word, $time);
     if (testbench.read_word != expected)
       begin
          $display("FAIL: UART Read = 0x%h NOT 0x%h @ %d", testbench.read_word[7:0], expected, $time);            
          `test_failed <= 1;            
       end 
      end
   endtask // uart_read_char
   

/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/   
   task uart_get_memory;
      input [31:0] address;      
      input [31:0] expected;
      
      begin
     `UART_WRITE_CHAR("G");
     `UART_WRITE_CHAR("e");
     `UART_WRITE_CHAR("T");
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR("M");
     `UART_WRITE_CHAR("e");
     `UART_WRITE_CHAR("m");
     `UART_WRITE_CHAR("o");
     `UART_WRITE_CHAR("R");
     `UART_WRITE_CHAR("y");
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR(convert_to_ascii(address[31:28]));
     `UART_WRITE_CHAR(convert_to_ascii(address[27:24]));
     `UART_WRITE_CHAR(convert_to_ascii(address[23:20]));
     `UART_WRITE_CHAR(convert_to_ascii(address[19:16]));
     `UART_WRITE_CHAR(convert_to_ascii(address[15:12]));
     `UART_WRITE_CHAR(convert_to_ascii(address[11:08]));
     `UART_WRITE_CHAR(convert_to_ascii(address[07:04]));
     `UART_WRITE_CHAR(convert_to_ascii(address[03:00]));
     @(posedge `UART_CLK);
     `UART_MASTER0.wb_wr1(32'hFFFF0000,    4'h0, {24'h000000, `CARRIAGE_RETURN});
//   `UART_PRESS_ENTER;


     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);

     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    
       
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    
       
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    
       
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);   
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    
       
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    
       
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    
       
     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    

     @(posedge testbench.uart0_int);
     `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
     $display("GET MEM: 0x%h == %c @ %d", testbench.read_word[7:0], testbench.read_word[7:0], $time);    

     
     `UART_READ_CHAR(`CARRIAGE_RETURN);      
     `UART_READ_CHAR(`LINE_FEED);        
//   `UART_READ_CHAR(convert_to_ascii(expected[31:28]));
//   `UART_READ_CHAR(convert_to_ascii(expected[27:24]));
//   `UART_READ_CHAR(convert_to_ascii(expected[23:20]));
//   `UART_READ_CHAR(convert_to_ascii(expected[19:16]));
//   `UART_READ_CHAR(convert_to_ascii(expected[15:12]));
//   `UART_READ_CHAR(convert_to_ascii(expected[11:08]));
//   `UART_READ_CHAR(convert_to_ascii(expected[07:04]));
//   `UART_READ_CHAR(convert_to_ascii(expected[03:00]));

      end
   endtask // uart_get_memory

/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/   
   task uart_dump_memory;
      input [31:0] address;      
      input[15:0] count;
      integer ii;
       
      begin
     `UART_WRITE_CHAR("d");
     `UART_WRITE_CHAR("u");
     `UART_WRITE_CHAR("m");
     `UART_WRITE_CHAR("p");
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR("M");
     `UART_WRITE_CHAR("e");
     `UART_WRITE_CHAR("m");
     `UART_WRITE_CHAR("o");
     `UART_WRITE_CHAR("R");
     `UART_WRITE_CHAR("y");
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR(convert_to_ascii(address[31:28]));
     `UART_WRITE_CHAR(convert_to_ascii(address[27:24]));
     `UART_WRITE_CHAR(convert_to_ascii(address[23:20]));
     `UART_WRITE_CHAR(convert_to_ascii(address[19:16]));
     `UART_WRITE_CHAR(convert_to_ascii(address[15:12]));
     `UART_WRITE_CHAR(convert_to_ascii(address[11:08]));
     `UART_WRITE_CHAR(convert_to_ascii(address[07:04]));
     `UART_WRITE_CHAR(convert_to_ascii(address[03:00]));
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR(convert_to_ascii(count[15:12]));
     `UART_WRITE_CHAR(convert_to_ascii(count[11:08]));
     `UART_WRITE_CHAR(convert_to_ascii(count[07:04]));
     `UART_WRITE_CHAR(convert_to_ascii(count[03:00]));
     `UART_PRESS_ENTER; 
     `UART_READ_CHAR("A");
     `UART_READ_CHAR("D");
     `UART_READ_CHAR("D");
     `UART_READ_CHAR("R");
     `UART_READ_CHAR("E");
     `UART_READ_CHAR("S");
     `UART_READ_CHAR("S");
     `UART_READ_CHAR(" ");
     `UART_READ_CHAR("D");
     `UART_READ_CHAR("A");
     `UART_READ_CHAR("T");
     `UART_READ_CHAR("A");
     `UART_READ_CHAR(" ");

     for (ii =0; ii<count; ii=ii+1)
       begin
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
          `UART_READ_CHAR(" ");
       end // for (ii<=0; ii<count; ii<=ii+1)    
     

      end
   endtask // uart_dump_memory
   
/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/   
   task uart_reset_ic;
       
      begin
     `UART_WRITE_CHAR("r");
     `UART_WRITE_CHAR("e");
     `UART_WRITE_CHAR("s");
     `UART_WRITE_CHAR("e");
     `UART_WRITE_CHAR("t");
     `UART_PRESS_ENTER;
      end
   endtask // uart_dump_memory
   

/***************************************************************************//**
@brief 

@param None

@retval None

 ******************************************************************************/   
   task uart_set_memory;
      input [31:0] address;      
      input [31:0] data;
      
      begin
     `UART_WRITE_CHAR("S");
     `UART_WRITE_CHAR("E");
     `UART_WRITE_CHAR("t");
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR("m");
     `UART_WRITE_CHAR("e");
     `UART_WRITE_CHAR("m");
     `UART_WRITE_CHAR("O");
     `UART_WRITE_CHAR("r");
     `UART_WRITE_CHAR("Y");
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR(convert_to_ascii(address[31:28]));
     `UART_WRITE_CHAR(convert_to_ascii(address[27:24]));
     `UART_WRITE_CHAR(convert_to_ascii(address[23:20]));
     `UART_WRITE_CHAR(convert_to_ascii(address[19:16]));
     `UART_WRITE_CHAR(convert_to_ascii(address[15:12]));
     `UART_WRITE_CHAR(convert_to_ascii(address[11:08]));
     `UART_WRITE_CHAR(convert_to_ascii(address[07:04]));
     `UART_WRITE_CHAR(convert_to_ascii(address[03:00]));
     `UART_WRITE_CHAR(" ");
     `UART_WRITE_CHAR(convert_to_ascii(data[31:28]));
     `UART_WRITE_CHAR(convert_to_ascii(data[27:24]));
     `UART_WRITE_CHAR(convert_to_ascii(data[23:20]));
     `UART_WRITE_CHAR(convert_to_ascii(data[19:16]));
     `UART_WRITE_CHAR(convert_to_ascii(data[15:12]));
     `UART_WRITE_CHAR(convert_to_ascii(data[11:08]));
     `UART_WRITE_CHAR(convert_to_ascii(data[07:04]));
     `UART_WRITE_CHAR(convert_to_ascii(data[03:00]));
     `UART_PRESS_ENTER;
     `UART_READ_CHAR(`LINE_FEED);    
//   `UART_READ_CHAR(`CARRIAGE_RETURN);

      end
   endtask // uart_set_memory






endmodule // uart_tasks   
