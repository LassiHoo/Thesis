import serial
from BasePlatform import basePlatform
from tcp_ip import ssh_connection
import time
import os
import pickle

class loraWanPlatfom(basePlatform):
    #these are LoraWan end node related configuration  and TX instruction set

    MacSet = "mac set "
    MacTx = "mac tx "
    Conf = "cnf "
    unConf = "uncnf "
    portnr = "1 "
    Appeui = "appeui BE7A000000000CDA"
    Appkey = "appkey 660625ED5FC16D37B82A5A0E9042CF0B"
    DevEui = "deveui 0004A30B001F3A95"
    macSave = "mac save"
    JoinOTaa = "mac join otaa\r\n"
    RLF = "\r\n"
    initFileName = "LPWAinitfile.dat"
    transmitFileName = "LPWATransmitfile.dat"
    START_TIME = 0
    SEND_INTERVAL = 1
    SEND_COUNT = 2
    PAYLOAD_LENGHT = 3
    TX_COMMAND = 4
    LINE_FEED = 5

    def createLoraWanTransmitlist(self):
        #creating list
        basePlatform.transmitterList.append(basePlatform.startTime)
        basePlatform.transmitterList.append(basePlatform.sendInterval)
        basePlatform.transmitterList.append(basePlatform.sendCount)
        basePlatform.transmitterList.append(basePlatform.payLoadLenght)
        # isolate these two into another list
        basePlatform.transmitterList.append(self.MacTx + self.Conf + self.portnr)
        basePlatform.transmitterList.append(self.RLF)


    def createInitList(self):
        #creating init list
        basePlatform.initList.append(self.MacSet + self.Appeui + self.RLF)
        basePlatform.initList.append(self.MacSet + self.Appkey + self.RLF)
        basePlatform.initList.append(self.MacSet + self.DevEui + self.RLF)
        basePlatform.initList.append(self.macSave + self.RLF)
        basePlatform.initList.append(self.JoinOTaa)

    def createInitializationFile(self):
        if not os.path.exists(self.initFileName):
            self.createInitList()
            source = open(self.initFileName,"wb")
            pickle.dump(basePlatform.initList, source)
            source.close()

    def createTransmitFile(self):
        if not os.path.exists(self.transmitFileName):
            self.createLoraWanTransmitlist()
            source = open(self.transmitFileName,"wb")
            pickle.dump(basePlatform.transmitterList, source)
            source.close()

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
        print(self.__transmitcommands[loraWanPlatfom.TX_COMMAND] + string + self.__transmitcommands[loraWanPlatfom.LINE_FEED] + "\n")
        self.__loraWanCom.write(self.__transmitcommands[loraWanPlatfom.TX_COMMAND] + string + self.__transmitcommands[loraWanPlatfom.LINE_FEED])
    def initInterface(self):
        for i in self.__initcommands:
            time.sleep(5)
            print(i)
            self.__loraWanCom.write(i)
        time.sleep(10)

    def start_gateway_logging(self):
        # log into gateway and start to tcp dump
        ssh = ssh_connection()
        ssh.Login('192.168.0.119', 'pi', 'raspberry')
        ssh.StartTCPdump("testfile.dat")
