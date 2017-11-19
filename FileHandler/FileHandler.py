import time
import pickle

class fileHandler:

    transmitterList = []
    sendInterval = 1
    payLoadLenght = 10
    startTime = ""

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

class LoraWANTransmitterListHandler(fileHandler):
    #these are LoraWan end node related configuration commands
    MacSet = "mac set "
    MacTx = "mac tx "
    Conf = "cnf "
    unConf = "uncnf "
    portnr = "1 "
    Appeui = "appeui BE7A000000000CDA"
    Appkey = "appkey 660625ED5FC16D37B82A5A0E9042CF0B"
    DevEui = "deveui 0004A30B001F3A95"
    macSave = "mac save"




#class NBiotTransmitterList