#! /usr/bin/env python3


import SerialPort

if __name__ == '__main__':


    serial_port = SerialPort.SerialPort()
    serial_port.open()
#    serial_port.transmit_binary([0x00, 0x01, 0x02, 0x03, 0x0D])
    serial_port.send_help()
    serial_port.close()
