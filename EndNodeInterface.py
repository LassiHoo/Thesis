import serial

class EndNode:

    def write(self, string):
        return True

class LoraWan:
    # this must be asked first in the start up
    Port = '/dev/ttyACM0'
    __loraWamCom = serial()
    def __init__(self, ):
        self.__loraWanCom = serial.Serial(port=self.Port,
                                   baudrate=57600, parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE,
                                   bytesize=serial.EIGHTBITS,
                                   timeout=1)

    def write(self,string):
        self.__loraWanCom.write(string)



