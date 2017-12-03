import serial
from EndNodeInitialization import loraWanPlatfom
from EndNodeInitialization import basePlatform


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
        self.__platForm.createLoraWanTransmitlist()
        self.__platForm.createInitList()

        self.__trasmitcommands = self.__init.readfile(self.__platForm.transmitFileName)
        self.__initcommands = self.__init.readfile(self.__platForm.initFileName)


    def transmit(self,string):
        self.__loraWanCom.write(self.__transmitcommands[4] + string + self.__transmitcommands[5])

    def initInterface(self):
        for i in self.__initcommands:
            self.__loraWamCom.write(i)

