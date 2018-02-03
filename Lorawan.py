import serial
from BasePlatform import basePlatform
from tcp_ip import ssh_connection
import time
import os
import pickle
import json

class loraWanPlatfom(basePlatform):
    #these are LoraWan end node related configuration  and TX instruction set



    TX_COMMAND = 0
    LINE_FEED = 1
    initFileName = "LPWAinitfile.json"
    transmitFileName = "LPWATransmitfile.json"
    def __init__(self):
        if not os.path.exists(self.initialization_json):
            #if file does not exists create a one
            self.data = {}
            self.data['transmit_parameters'] = []
            self.data['transmit_parameters'].append({
                'start_time': 'none',
                'send_interval_milliseconds': 8000,
                'send_count': 10000,
                'send_forever': 'true',
                'status': 'waitin_to_start',
                'interval_decrement_milliseconds': 100,
                'data_content': 'from_diagnostic_frame'
            })
            with open('data.txt', 'w') as self.initialization_json:
                json.dump(self.data, self.initialization_json)
        else:
            self.data = json.load(self.intialization_json)

    def createLoraWanTransmitlist(self):
        #creating list
        # isolate these two into another list
        basePlatform.transmitterList.append(self.MacTx + self.unConf + self.portnr)
        basePlatform.transmitterList.append(self.RLF)


    def createInitList(self):
        #creating init list
        basePlatform.initList.append("sys factoryRESET" + self.RLF)
        basePlatform.initList.append(self.data['factoryreset'] + self.data['RLF'])
        basePlatform.initList.append(self.data['RadioSet'] + self.data['prlen'] + self.data['RLF'])
        basePlatform.initList.append(self.data['RadioSet'] + self.data['sf8'] + self.data['RLF'])
        basePlatform.initList.append(self.data['MacSet'] + self.data['Appeui'] + self.data['Appeui_val'] + self.data['RLF'])
        basePlatform.initList.append(self.data['MacSet'] + self.data['Appkey'] + self.data['Appkey_val'] + self.data['RLF'])
        basePlatform.initList.append(self.data['MacSet'] + self.data['DevEui'] + self.data['DevEui_val']+ self.data['RLF'])
        basePlatform.initList.append(self.data['MacSet'] + self.data['DevAddr'] + self.data['DevAddr_val'] + self.data['RLF'])
        basePlatform.initList.append(self.data['macSave'] + self.data['RLF'])
        basePlatform.initList.append(self.data['JoinOTaa'])

    def createInitializationFile(self):
        if not os.path.exists(self.initFileName):
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
                'DevAddr_val':'1',
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
            with open('data.txt', 'w') as self.initFileName:
                json.dump(self.data, self.initFileName)

    def createTransmitFile(self):
        if not os.path.exists(self.transmitFileName):
            self.data = {}
            self.data['Lorawan_settings'] = []
            self.data['Lorawan.settings'].append({
                'Appeui': 'appeui BE7A000000000CDA',
                'Appkey': 'appkey 660625ED5FC16D37B82A5A0E9042CF0B',
            })
            with open('data.txt', 'w') as self.transmitFileName:
                json.dump(self.data, self.transmitFileName)

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
        self.__platForm.createTransmitFile()
        self.__platForm.createInitializationFile()

        self.__transmitcommands = self.__init.readfile(self.__platForm.transmitFileName)
        for i in self.__transmitcommands:
            print (i)
        self.__initcommands = self.__init.readfile(self.__platForm.initFileName)
        for i in self.__initcommands:
            print (i)
        self.ssh = ssh_connection()

    def transmit(self,string):
        print(self.__transmitcommands[loraWanPlatfom.TX_COMMAND] + string + self.__transmitcommands[loraWanPlatfom.LINE_FEED] + "\n")
        self.__loraWanCom.write(self.__transmitcommands[loraWanPlatfom.TX_COMMAND] + string + self.__transmitcommands[loraWanPlatfom.LINE_FEED])
    def initInterface(self):
        for i in self.__initcommands:
            time.sleep(4)
            print(i)
            self.__loraWanCom.write(i)
        time.sleep(7)

    def start_gateway_logging(self):
        # log into gateway and start to tcp dump

        self.ssh.Login('192.168.0.119', 'pi', 'raspberry')
        self.ssh.StartTCPdump("testfile.dat")
        time.sleep(5)

    def stop_gateway_logging(self):
        # log into gateway and start to tcp dump
        self.ssh.StopTCPdump()
        self.ssh.GetTCPdumpFile('pi','testfile.dat','192.168.0.119')
        self.ssh.CloseConnection()
