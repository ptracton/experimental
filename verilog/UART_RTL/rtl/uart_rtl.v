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
   tx, irq, busy, rx_byte, tx_fifo_full,
   // Inputs
   clk, rst, rx, transmit, tx_byte, rx_fifo_pop
   ) ;

   input clk;
   input rst;
   input rx;
   input transmit;
   input [7:0] tx_byte;
   input       rx_fifo_pop;

   output      tx;
   output      irq;
   output      busy;
   output [7:0] rx_byte;
   output       tx_fifo_full;

   /*AUTOREG*/


   /*AUTOWIRE*/
   // Beginning of automatic wires (for undeclared instantiated-module outputs)
   wire                 is_receiving;           // From uart_inst of uart.v
   wire                 is_transmitting;        // From uart_inst of uart.v
   wire                 received;               // From uart_inst of uart.v
   wire                 recv_error;             // From uart_inst of uart.v
   // End of automatics


   wire                 rx_fifo_full;
   wire [7:0]           rx_fifo_data_in;  //From UART to FIFO
   wire                 rx_fifo_pop;


   wire [7:0]           tx_fifo_data_out; //From FIFO to UART
   wire                 tx_fifo_full;
   wire                 tx_fifo_empty;
   reg                  tx_fifo_pop;

   reg                  uart_transmit;


   assign irq = received || recv_error || rx_fifo_full;
   assign busy = is_receiving || is_transmitting;

   //
   // UART Instance.  Handles the actual sending/receiving of serial data
   //
   uart uart_inst(/*AUTOINST*/
                  // Outputs
                  .tx                   (tx),
                  .received             (received),
                  .rx_byte              (rx_fifo_data_in),
                  .is_receiving         (is_receiving),
                  .is_transmitting      (is_transmitting),
                  .recv_error           (recv_error),
                  // Inputs
                  .clk                  (clk),
                  .rst                  (rst),
                  .rx                   (rx),
                  .transmit             (uart_transmit),
                  .tx_byte              (tx_fifo_data_out));


   //
   // RX FIFO takes data recevied by the UART and holds until outside module
   // requests data
   //
   fifo #(.DATA_WIDTH(8))
   rx_fifo(
           // Outputs
           .DATA_OUT               (rx_byte),
           .FULL                   (rx_fifo_full),
           .EMPTY                  (),
           // Inputs
           .CLK                    (clk),
           .RESET                  (rst),
           .ENABLE                 (1'b1),
           .FLUSH                  (1'b0),
           .DATA_IN                (rx_fifo_data_in),
           .PUSH                   (received),
           .POP                    (rx_fifo_pop));


   //
   // TX FIFO takes data from outside module and holds it until the
   // UART is able to transmit it
   //
   fifo #(.DATA_WIDTH(8))
   tx_fifo(
           // Outputs
           .DATA_OUT               (tx_fifo_data_out),
           .FULL                   (tx_fifo_full),
           .EMPTY                  (tx_fifo_empty),
           // Inputs
           .CLK                    (clk),
           .RESET                  (rst),
           .ENABLE                 (1'b1),
           .FLUSH                  (1'b0),
           .DATA_IN                (tx_byte),
           .PUSH                   (transmit),
           .POP                    (tx_fifo_pop));

   //
   // POP from TX FIFO is it is NOT empty and we are NOT transmitting
   //
   always @(posedge clk)
     if (rst) begin
        tx_fifo_pop <= 1'b0;
     end else begin
        if (tx_fifo_empty ==0 & is_transmitting == 0)
          tx_fifo_pop <= 1'b1;
        else
          tx_fifo_pop <= 1'b0;
     end


   //
   // Delay the transmit signal to the UART by 1 clock
   // to let data propagate through the FIFO
   //
   always @(posedge clk)
     if (rst) begin
        uart_transmit <= 1'b0;
     end else begin
        uart_transmit <= transmit;
     end


endmodule // uart_rtl
