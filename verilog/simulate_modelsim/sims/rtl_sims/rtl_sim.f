vlib work
vlog ../../bench/verilog/testbench.v
vlog ../../bench/verilog/dump.v
vlog ../../rtl/verilog/top_level.v 
#-do ../../rtl/verilog/top_level.f
vsim -voptargs=+acc work.testbench +define+XILINX   
run -all
