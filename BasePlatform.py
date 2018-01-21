import os
import pickle


class basePlatform:

    transmitterList = []
    initList=[]
    commandIndex=[]
    # milliseconds
    sendInterval = 8000
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



#class NBiotTransmitterList