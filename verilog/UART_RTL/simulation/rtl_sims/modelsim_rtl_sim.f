vlib work

vlog ../../tasks/uart_tasks.v
vlog ../../testbench/testbench.v 
vlog ../../testbench/dump.v

vlog ../../behavioral/wb_uart/uart_regs.v
vlog ../../behavioral/wb_uart/uart_rfifo.v
vlog ../../behavioral/wb_uart/uart_sync_flops.v
vlog ../../behavioral/wb_uart/uart_tfifo.v
vlog ../../behavioral/wb_uart/uart_top.v
vlog ../../behavioral/wb_uart/uart_transmitter.v
vlog ../../behavioral/wb_uart/uart_wb.v

vlog ../../rtl/uart.v
vlog ../../rtl/uart_rtl.v
vlog ../../rtl/fifo.v

vsim -voptargs=+acc work.testbench +define+ALTERA  
run -all
