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

    def seek_transmissionnumber_delay(self, transmissionnumber):
        csv_file = csv.reader(open(self.csv_filename[0], "rb"), delimiter=",")

        for row in csv_file:
            list = row[15].split('-')
            if list[0] != "payload":
                number = int(list[1][4:6],16)
                print ("csv number: ",number,"seek number: ",transmissionnumber)
                if number == transmissionnumber and row[7] != "CRC_BAD":
                    print ("found number, row: ",row)
                    rest, millisecond = row[2].split(".")
                    r = ''.join(c for c in millisecond if c != 'Z')
                    restr, minute, second = rest.split(":")
                    second_to_millisecond = 1000 * int(second)
                    minute_to_millisecond = 60 * int(minute) * 1000
                    total_milliseconds = int(r) + minute_to_millisecond + second_to_millisecond
                    rssi = row[13]
                    cr = row[12]
                    SF = row[11]
                    snr = row[14]
                    return total_milliseconds, rssi , cr ,SF,snr
        return 0

    def calculate_delays(self,transmitlist):
        DELAY=[]
        SNR=[]
        RSSI=[]
        SF = []
        CR = []
        packet_lost_count = 0
        transmit_number = 0
        for index, item in enumerate(transmitlist):
            #print(index,item)
            found_delay, rssi,cr,sf,snr = self.seek_transmissionnumber_delay(index)
            #print ("gateawydelay: ", found_delay ," transmit delay: ", item, "transmitnumber", index)
            if ( found_delay != 0):
                DELAY.append(found_delay - item)
                SNR.append(snr)
                RSSI.append(rssi)
                CR.append(cr)
                SF.append(sf)
            else:
                packet_lost_count += packet_lost_count
                transmit_number = index
        if packet_lost_count == 0:
             PER = 0
        else:
             PER =  packet_lost_count/transmit_number *100
        SNR = [float(a) for a in SNR]
        RSSI = [int(b) for b in RSSI]
        return DELAY, SNR, RSSI, CR, SF, PER