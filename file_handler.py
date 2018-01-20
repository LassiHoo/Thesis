import pickle
import os
import fnmatch
import csv

class file_hander:

    def __init__(self, transmitterfilename):
        self.transmitDataList=[]
        self.transmitterFileName = transmitterfilename
        self.csv_filename=[]
    def addTxData(self,data,timestamp):
        tuple = timestamp,data
        self.transmitDataList.append(tuple)

    def strore_data(self):
        source = open(self.transmitterFileName,"wb")
        pickle.dump(self.transmitDataList, source)
        source.close()

    def read_file(self, filename):
        try:
            file = open(filename, "rb")
            read = pickle.load(file)
            return read
        except IOError:
            print("Could not open the file")
            return False

    def return_csv_filename(self):
        files = filter(os.path.isfile, os.listdir(os.curdir))
        test = fnmatch.filter(files, '*csv*')
        print("searching csv files:",test)
        self.csv_filename = fnmatch.filter(files, '*csv*')

    def seek_transmission_delay_data_from_csv_file(self, value):
        returnlist=[]
        csv_file = csv.reader(open(self.csv_filename[0], "rb"), delimiter=",")
        #print(value)
        # loop through csv list
        for row in csv_file:
            if row[0] != "gateway ID":
                rest, millisecond = row[2].split(".")
                r=''.join(c for c in millisecond if c != 'Z')
                restr,minute,second = rest.split(":")
                second_to_millisecond = 1000*int(second)
                minute_to_millisecond = 60*int(minute)*1000
                total_milliseconds = int(r) + minute_to_millisecond + second_to_millisecond
                returnlist.append(total_milliseconds)
        return returnlist

    def seek_transmissionnumber_delay(self, transmissionnumber):
        csv_file = csv.reader(open(self.csv_filename[0], "rb"), delimiter=",")

        for row in csv_file:
            list = row[15].split('-')
            if list[0] != "payload":
                number = int(list[1][4:6],16)
                print ("csv number: ",number,"seek number: ",transmissionnumber)
                if number == transmissionnumber:
                    print ("found number, row: ",row)
                    rest, millisecond = row[2].split(".")
                    r = ''.join(c for c in millisecond if c != 'Z')
                    restr, minute, second = rest.split(":")
                    second_to_millisecond = 1000 * int(second)
                    minute_to_millisecond = 60 * int(minute) * 1000
                    total_milliseconds = int(r) + minute_to_millisecond + second_to_millisecond
                    return total_milliseconds
        return 0

    def calculate_delays(self,transmitlist):
        transmitnumber = 0
        delay=[]
        for i in transmitlist:
            found_delay = self.seek_transmissionnumber_delay(transmitnumber)
            print ("gateawydelay: ", found_delay ," transmit delay: ", i, "transmitnumber", transmitnumber)
            delay.append(found_delay-i)
            transmitnumber += 1
        return delay





    def seek_RSSI_data_from_csv_file(self):
        returnlist = []
        csv_file = csv.reader(open(self.csv_filename[0], "rb"), delimiter=",")
        # print(value)
        # loop through csv list
        for row in csv_file:
            # if current rows 2nd value is equal to input, print that row
            returnlist.append(row[13])
        returnlist.pop(0)
        returnlist = [int(a) for a in returnlist]
        return returnlist

    def seek_SNR_data_from_csv_file(self):
        returnlist = []
        csv_file = csv.reader(open(self.csv_filename[0], "rb"), delimiter=",")
        # print(value)
        # loop through csv list
        for row in csv_file:
            # if current rows 2nd value is equal to input, print that row
            returnlist.append(row[14])
        returnlist.pop(0)
        returnlist = [float(a) for a in returnlist]
        return returnlist