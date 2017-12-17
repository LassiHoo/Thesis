import serial
from EndNodeInitialization import loraWanPlatfom
from EndNodeInitialization import basePlatform
from FileHandler import FileHandler


class LoraWan:
    # this must be asked first in the start up
    Port = '/dev/ttyACM0'
    __platForm = loraWanPlatfom()
    __init = basePlatform()
    __initcommands=[]
    __transmitcommands=[]

    def __init__(self, ):
        self.__loraWanCom = serial.Serial(port=self.Port,
                                   baudrate=57600, parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE,
                                   bytesize=serial.EIGHTBITS,
                                   timeout=1)

        # create transmit and initializaiotn files if they do not exists
        self.__platForm.createTransmitFile()
        self.__platForm.createInitializationFile()

        self.__transmitcommands = self.__init.readfile(self.__platForm.transmitFileName)
        for i in self.__transmitcommands:
            print i
        self.__initcommands = self.__init.readfile(self.__platForm.initFileName)
        for i in self.__initcommands:
            print i

    def transmit(self,string):
        self.__loraWanCom.write(self.__transmitcommands[loraWanPlatfom.TX_COMMAND] + string + self.__transmitcommands[loraWanPlatfom.LINE_FEED])

    def initInterface(self):
        for i in self.__initcommands:
            self.__loraWanCom.write(i)

