//                              -*- Mode: Verilog -*-
// Filename        : testbench.v
// Description     : UART RTL Test bench
// Author          : Philip Tracton
// Created On      : Mon Apr 20 16:05:13 2015
// Last Modified By: Philip Tracton
// Last Modified On: Mon Apr 20 16:05:13 2015
// Update Count    : 0
// Status          : Unknown, Use with caution!

module testbench (/*AUTOARG*/ ) ;

   //
   // Free Running 50 MHz Clock
   //
   reg clk_tb;

   parameter   _clk_50mhz_high = 10,
     _clk_50mhz_low  = 10,
     _clk_50mhz_period = _clk_50mhz_high + _clk_50mhz_low;

   initial
     begin
        clk_tb <= 'b0;
        forever
          begin
             #(_clk_50mhz_low)  clk_tb = 1;
             #(_clk_50mhz_high) clk_tb = 0;
          end
     end

   //
   // Asynch. Reset to device
   //
   reg reset_tb;
   initial
     begin
        reset_tb = 0;
        #1    reset_tb = 1;
        #200  reset_tb = 0;
     end
   wire uart_irq;
   reg  transmit;
   reg [7:0] tx_byte;
   wire      busy;
   wire [7:0] rx_byte;

   uart_rtl dut(
                .tx(UART0_TX),
                .clk(clk_tb),
                .rst(reset_tb),
                .rx(UART0_RX),
                .irq(uart_irq),
                .transmit(transmit),
                .tx_byte(tx_byte),
                .busy(busy),
                .rx_byte(rx_byte)
                ) ;

   //
   // Simulation tools
   //
   reg test_failed;
   reg [31:0] read_word;
   initial begin
      test_failed <= 1'b0;
      read_word <= 32'b0;
   end

   /****************************************************************************
    UART 0 -- This is used for CLI Interfacing

    The WB UART16550 from opencores is used here to simulate a UART on the other end
    of the cable.  It will allow us to send/receive characters to the NGMCU firmware
    ***************************************************************************/

   wire [31:0] uart0_adr;
   wire [31:0] uart0_dat_o;
   wire [31:0] uart0_dat_i;
   wire [3:0]  uart0_sel;
   wire        uart0_cyc;
   wire        uart0_stb;
   wire        uart0_we;
   wire        uart0_ack;
   wire        uart0_int;



   assign      uart0_dat_o[31:8] = 'b0;



   uart_top uart0(
                  .wb_clk_i(clk_tb),
                  .wb_rst_i(reset_tb),

                  .wb_adr_i(uart0_adr[4:0]),
                  .wb_dat_o(uart0_dat_o),
                  .wb_dat_i(uart0_dat_i),
                  .wb_sel_i(uart0_sel),
                  .wb_cyc_i(uart0_cyc),
                  .wb_stb_i(uart0_stb),
                  .wb_we_i(uart0_we),
                  .wb_ack_o(uart0_ack),
                  .int_o(uart0_int),
                  .stx_pad_o(UART0_RX),
                  .srx_pad_i(UART0_TX),

                  .rts_pad_o(),
                  .cts_pad_i(1'b0),
                  .dtr_pad_o(),
                  .dsr_pad_i(1'b0),
                  .ri_pad_i(1'b0),
                  .dcd_pad_i(1'b0),

                  .baud_o()
                  );


   wb_mast uart_master0(
                        .clk (clk_tb),
                        .rst (reset_tb),
                        .adr (uart0_adr),
                        .din (uart0_dat_o),
                        .dout(uart0_dat_i),
                        .cyc (uart0_cyc),
                        .stb (uart0_stb),
                        .sel (uart0_sel),
                        .we  (uart0_we ),
                        .ack (uart0_ack),
                        .err (1'b0),
                        .rty (1'b0)
                        );


   //
   // Test Case
   //
   initial begin
      tx_byte <= 8'h00;
      transmit <= 1'b0;

      @(negedge reset_tb);
      $display("RESET RELEASED %d", $time);
      repeat(10)@(posedge clk_tb);


      `UART_CONFIG();
      `UART_WRITE_CHAR("A");
      `UART_WRITE_CHAR("B");
      `UART_WRITE_CHAR("C");

      repeat(10)@(posedge clk_tb);

      `UART_READ_CHAR("X");
      `UART_READ_CHAR("Y");
      `UART_READ_CHAR("Z");

      repeat(100)@(posedge clk_tb);
      $finish;

   end
endmodule // testbench
