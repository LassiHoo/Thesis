import serial

class EndNode:

    def write(self, string):

class LoraWan:

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



