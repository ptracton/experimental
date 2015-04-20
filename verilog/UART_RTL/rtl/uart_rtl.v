//                              -*- Mode: Verilog -*-
// Filename        : uart_rtl.v
// Description     : UART RTL Example
// Author          : Philip Tracton
// Created On      : Mon Apr 20 16:00:09 2015
// Last Modified By: Philip Tracton
// Last Modified On: Mon Apr 20 16:00:09 2015
// Update Count    : 0
// Status          : Unknown, Use with caution!


module uart_rtl (/*AUTOARG*/
   // Outputs
   tx,
   // Inputs
   clk, rst, rx
   ) ;

   input clk;
   input rst;
   input rx;
   output tx;

   /*AUTOREG*/


   /*AUTOWIRE*/
   // Beginning of automatic wires (for undeclared instantiated-module outputs)
   wire                 is_receiving;           // From uart_inst of uart.v
   wire                 is_transmitting;        // From uart_inst of uart.v
   wire                 received;               // From uart_inst of uart.v
   wire                 recv_error;             // From uart_inst of uart.v
   wire [7:0]           rx_byte;                // From uart_inst of uart.v
   // End of automatics

   reg                  transmit;
   reg [7:0]            tx_byte;


   uart uart_inst(/*AUTOINST*/
                  // Outputs
                  .tx                   (tx),
                  .received             (received),
                  .rx_byte              (rx_byte[7:0]),
                  .is_receiving         (is_receiving),
                  .is_transmitting      (is_transmitting),
                  .recv_error           (recv_error),
                  // Inputs
                  .clk                  (clk),
                  .rst                  (rst),
                  .rx                   (rx),
                  .transmit             (transmit),
                  .tx_byte              (tx_byte[7:0]));



endmodule // uart_rtl
