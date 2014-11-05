#! /usr/bin/env python3


import SerialPort

if __name__ == '__main__':

    serial_port = SerialPort.SerialPort()
    serial_port.open()
    serial_port.transmit_binary([0x03])
#    serial_port.send_help()
    serial_port.close()
