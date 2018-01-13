import pickle


class file_hander:

    def __init__(self, transmitterfilename):
        self.transmitDataList=[]
        self.transmitterFileName = transmitterfilename
    def addTxData(self,data,timestamp):
        tuple = timestamp,data
        self.transmitDataList.append(tuple)

    def stroredata(self):
        source = open(self.transmitterFileName,"wb")
        pickle.dump(self.transmitDataList, source)
        source.close()
