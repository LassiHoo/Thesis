from EndNodeInitialization import loraWANFileHandler
from EndNodeInitialization import fileHandler
from EndNodeInterface import LoraWan

def main():

    platForm = loraWANFileHandler()
    #create transmit and initializaiotn files if they do not exists
    platForm.createLoraWanTransmitlist()
    platForm.createInitList()
    Init=fileHandler()
    trasmitcommands = Init.readfile(platForm.transmitFileName)
    initcommands = Init.readfile(platForm.initFileName)
    endnodeInterFace = LoraWan()

    for i in initcommands:
        endnodeInterFace.write(i)






if __name__ == "__main__":
    main()