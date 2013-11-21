
import serial
import array

class SerialPort (serial.Serial):
    

    def __init__(self):
        serial.Serial.__init__(self)

        settings =self.getSettingsDict()
        self.applySettingsDict(settings)
        self.baudrate=115200    
        self.port = "COM9"
             
        pass
    
    def calculate_crc(self, data):
        crc = 0
        for x in data:
            crc += x

        return crc

    def transmit_binary(self, data):
        #
        # http://stackoverflow.com/questions/472977/binary-data-with-pyserialpython-serial-port
        #
        
        transmit = array.array('B', data).tostring()
        print (transmit)
        self.write(transmit)

    def send_ping(self):
        packet = [0x0C, 0x03, 0xF0, 0xAA, 0x00]
        print (packet)
        crc = self.calculate_crc(packet)
        crc =  crc.to_bytes(2, byteorder='big')
        print (crc)
        for x in crc:
            print (x)
            packet.append(x)
        packet.append(0x0D)
        print(packet)
        self.transmit_binary(packet)

    def character(self, b):
        return b.decode('latin1')

    def send_help(self):
        packet = [0x68, 0x65, 0x6C, 0x70, 0x0D]
        self.transmit_binary(packet)
        while (1):
            data = self.character(self.read(1))
            print (data)
