import time
import pickle

class fileHandler:

    transmitterList = []
    initList=[]
    commandIndex=[]
    sendInterval = 1
    sendCount = 10
    payLoadLenght = 10
    startTime = ""
    isDutyCycleOn = false

    def dutyCycleOn():
        #create dutyCycle calcutalion here
        return False


    def fileHandleOpen(name, RW, errorString, dump):
        #opens a transmitter or initialization file
        try:
            source = open(name, RW)
            return source
        except IOError:
            print(errorString)
            source = open(name, 'wb')
            pickle.dump(dump, source)
            return source

class loraWANTxListHandler(fileHandler):
    #these are LoraWan end node related configuration  and TX send commands
    #

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

    def commandIndex(self):

        fileHandler.commandIndex = "START_TIME" "SEND_INTERVAL" "SEND_COUNT" "PAYLOAD_LENGHT" "TX_COMMAND""LINE_FEED"

    def  createLoraWanTransmitFile(self):
        #creating list
        fileHandler.transmitterList.append(fileHandler.startTime)
        fileHandler.transmitterList.append(fileHandler.sendInterval)
        fileHandler.transmitterList.append(fileHandler.sendCount)
        fileHandler.transmitterList.append(fileHandler.payLoadLenght)
        fileHandler.transmitterList.append(self.MacTx + self.portnr )
        fileHandler.transmitterList.append(self.RLF)

    def createInitList(self):
        #creating init list
        fileHandler.initList.append(self.MacSet + self.Appeui + self.RLF )
        fileHandler.initList.append(self.MacSet + self.Appkey + self.RLF)
        fileHandler.initList.append(self.MacSet + self.DevEui + self.RLF)
        fileHandler.initList.append(self.macSave + self.RLF)

#class NBiotTransmitterList