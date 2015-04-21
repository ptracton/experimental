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

   //
   // Configure WB UART in testbench
   // 115200, 8N1
   //
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


   //
   // Write a character to WB UART and catch with FPGA UART
   //
   task uart_write_char;
      input [7:0] char;
      begin
         @(posedge `UART_CLK);
         $display("TASK: UART Write = %c @ %d", char, $time);
         `UART_MASTER0.wb_wr1(32'hFFFF0000,    4'h0, {24'h000000, char});

         if (testbench.busy == 0)begin
            @(posedge testbench.busy);
         end

         while(testbench.busy == 1'b1)begin
            #1;

         end

         if (testbench.rx_byte != char)
           begin
              $display("FAIL: UART Write = 0x%h NOT 0x%h @ %d", testbench.rx_byte, char, $time);
              `test_failed <= 1;
           end
         //         `wait(1`mS);
      end
   endtask // uart_write_char

   //
   // Read a character with WB UART that was sent from FPGA UART
   //
   task uart_read_char;
      input [7:0] expected;
      begin
         testbench.tx_byte = expected;
         testbench.transmit <= 1;
         @(posedge `UART_CLK);
         testbench.transmit <= 0;

         if (testbench.busy == 0)begin
            @(posedge testbench.busy);
         end

         while(testbench.busy == 1'b1)begin
            #1;

         end

         `UART_MASTER0.wb_rd1(32'hFFFF0000,    4'h0, testbench.read_word);
         $display("\033[93mTASK: UART Read = %c @ %d", testbench.read_word, $time);
         if (testbench.read_word != expected)
           begin
              $display("\033[1;31mFAIL: UART Read = 0x%h NOT 0x%h @ %d\033[0m", testbench.read_word[7:0], expected, $time);
              `test_failed <= 1;
           end
      end
   endtask // uart_read_char





endmodule // uart_tasks   
