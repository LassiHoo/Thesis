import serial
from BasePlatform import basePlatform
#from tcp_ip import ssh_connection
import time
import os
import json

class loraWanPlatfom(basePlatform):
    #these are LoraWan end node related configuration  and TX instruction set



    TX_COMMAND = 0
    LINE_FEED = 1
    initFileName = "LPWAinitfile.jso"
    transmitFileName = "Txfile.jso"
    def __init__(self):
        if not os.path.exists(self.transmitFileName):
            # if file does not exists create a one
            self.data = {}
            self.data['Lorawan_settings'] = []
            self.data['Lorawan_settings'].append({
                'Appeui': 'appeui ',
                'Appeui_val' : 'BE7A000000000CDA',
                'Appkey': 'appkey ',
                'Appkey_val': '660625ED5FC16D37B82A5A0E9042CF0B',
                'DevEui': 'deveui ',
                'DevEui_val':'0004A30B001F3A95',
                'DevAddr': 'devaddr ',
                'DevAddr_val':'00000001',#in hexadecimal form
                'macSave': 'mac save',
                'JoinOTaa': 'mac join otaa\r\n',
                'data_content': 'from_diagnostic_frame',
                'RLF': '\r\n',
                'RadioSet': 'radio set ',
                'portnr': '1 ',
                'MacSet' : 'mac set ',
                'SysSet': 'sys set',
                'MacTx': 'mac tx ',
                'Conf' : 'cnf ',
                'unConf' : 'uncnf ',
                'prlen' : 'prlen 16',
                'sf8' : 'sf sf8',
                'factoryreset':'sys factoryRESET'
            })
            with open(self.transmitFileName, 'w') as outfile:
                json.dump(self.data, outfile)
        else:
            with open(self.transmitFileName, 'r') as infile:
                self.data = json.load(infile)

    def createLoraWanTransmitlist(self):
        #creating list
        # isolate these two into another list
        basePlatform.transmitterList.append(self.data['Lorawan_settings'][0]['MacTx'] + self.data['Lorawan_settings'][0]['unConf'] + self.data['Lorawan_settings'][0]['portnr'])
        basePlatform.transmitterList.append(self.data['Lorawan_settings'][0]['RLF'])


    def createInitList(self):
        #creating init list
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['factoryreset'] + self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['RadioSet'] + self.data['Lorawan_settings'][0]['prlen'] + self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['RadioSet'] + self.data['Lorawan_settings'][0]['sf8'] + self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['MacSet'] + self.data['Lorawan_settings'][0]['Appeui'] + self.data['Lorawan_settings'][0]['Appeui_val'] + self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['MacSet'] + self.data['Lorawan_settings'][0]['Appkey'] + self.data['Lorawan_settings'][0]['Appkey_val'] + self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['MacSet'] + self.data['Lorawan_settings'][0]['DevEui'] + self.data['Lorawan_settings'][0]['DevEui_val']+ self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['MacSet'] + self.data['Lorawan_settings'][0]['DevAddr'] + self.data['Lorawan_settings'][0]['DevAddr_val'] + self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['macSave'] + self.data['Lorawan_settings'][0]['RLF'])
        basePlatform.initList.append(self.data['Lorawan_settings'][0]['JoinOTaa'])

class LoraWan():

    # this must be asked first in the start up
    Port = '/dev/ttyACM0'
    __platForm = loraWanPlatfom()
    __init = basePlatform()
    __initcommands=[]
    __transmitcommands=[]
    transmitFileName=__platForm.transmitFileName

    def __init__(self, ):
        self.__loraWanCom = serial.Serial(port=self.Port,
                                   baudrate=57600, parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE,
                                   bytesize=serial.EIGHTBITS,
                                   timeout=1)

        # create transmit and initializaiotn files if they do not exists
        self.__platForm.createLoraWanTransmitlist()
        self.__platForm.createInitList()
        self.__transmitcommands = self.__init.transmitterList
        for i in self.__transmitcommands:
            print (i)
        self.__initcommands = self.__init.initList
        for i in self.__initcommands:
            print (i)

    def transmit(self,string):
        txdata = self.__transmitcommands[loraWanPlatfom.TX_COMMAND] + string + self.__transmitcommands[loraWanPlatfom.LINE_FEED]
        print(txdata)
        self.__loraWanCom.write(txdata.encode())
    def initInterface(self):
        for i in self.__initcommands:
            time.sleep(4)
            print(i)
            self.__loraWanCom.write(i.encode())
        time.sleep(10)
