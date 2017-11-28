import os
import pickle

class basePlatform:

    transmitterList = []
    initList=[]
    commandIndex=[]
    sendInterval = 1
    sendCount = 10
    payLoadLenght = 10
    startTime = ""
    isDutyCycleOn = False

    def dutyCycleOn():
        #create dutyCycle calculation here
        return False

    def readfile(self,filename):
        try:
            file = open(filename, "rb")
            read = pickle.load(file)
            return read
        except IOError:
            print("Could not open the file")
            return False

    def fileHandleOpen(name):
        #opens a transmitter or initialization file
        try:
            source = open(name, "rw")
            return source
        except IOError:
            print("Could not open the file")
            return False

class loraWanPlatfom(basePlatform):
    #these are LoraWan end node related configuration  and TX send commands

    MacSet = "mac set "
    MacTx = "mac tx "
    Conf = "cnf "
    unConf = "uncnf "
    portnr = "1 "
    Appeui = "appeui BE7A000000000CDA"
    Appkey = "appkey 660625ED5FC16D37B82A5A0E9042CF0B"
    DevEui = "deveui 0004A30B001F3A95"
    macSave = "mac save"
    RLF = "\r\n"
    initFileName = "LPWAinitfile.dat"
    transmitFileName = "LPWATransmitfile.dat"

    def commandIndex(self):
        basePlatform.commandIndex = "START_TIME" "SEND_INTERVAL" "SEND_COUNT" "PAYLOAD_LENGHT" "TX_COMMAND""LINE_FEED"

    def createLoraWanTransmitlist(self):
        #creating list
        basePlatform.transmitterList.append(basePlatform.startTime)
        basePlatform.transmitterList.append(basePlatform.sendInterval)
        basePlatform.transmitterList.append(basePlatform.sendCount)
        basePlatform.transmitterList.append(basePlatform.payLoadLenght)
        basePlatform.transmitterList.append(self.MacTx + self.portnr)
        basePlatform.transmitterList.append(self.RLF)

    def createInitList(self):
        #creating init list
        basePlatform.initList.append(self.MacSet + self.Appeui + self.RLF)
        basePlatform.initList.append(self.MacSet + self.Appkey + self.RLF)
        basePlatform.initList.append(self.MacSet + self.DevEui + self.RLF)
        basePlatform.initList.append(self.macSave + self.RLF)

    def createInitializationFile(self):
        if not os.path.exists(self.initFileName):
            self.createInitList()
            source = open(self.initFileName)
            pickle.dump(basePlatform.initList, source)
            source.close()

    def createTransmitFile(self):
        if not os.path.exists(self.transmitFileName):
            self.createLoraWanTransmitlist()
            source = open(self.transmitFileName)
            pickle.dump(basePlatform.transmitterList, source)
            source.close()

#class NBiotTransmitterList