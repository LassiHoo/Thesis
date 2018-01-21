from BasePlatform import basePlatform
from Lorawan import LoraWan
from file_handler import file_hander
import os
import datetime
import random
import time
from Graph import graph


def main():

    transmit_settings = basePlatform()
    lpwa_interface = LoraWan()
    transmit_log_file = file_hander("transmitLogfile.dat")
    lpwa_interface.initInterface()
    print( lpwa_interface.transmitFileName )
    while not os.path.exists(lpwa_interface.transmitFileName):
        print ("waiting transmit file")



    lpwa_interface.start_gateway_logging()
    time.sleep(10)

    timenow = datetime.datetime.now()
    print("waiting for start time, time now: ", timenow.microsecond, " start time ", transmit_settings.startTime)
    #while (timenow.microseconds < transmit_settings.startTime):
    #    print( "waiting for start time, time now: ",timenow.microseconds," start time ",transmit_settings.startTime)
    #    timenow = datetime.now()
    trdelay = []
    transmissioncount=[]
    wapice_test_line_hex = ''
    for i in range (0, 10):
         time.sleep(transmit_settings.sendInterval)
         transmissioncount.append(i)
         date = datetime.datetime.utcnow()
         total_milliseconds = ( date.microsecond / 1000) + ( date.minute * 60 * 1000 ) + (date.second * 1000)
         add = hex(random.randint(0,20))[2:]
         wapice_test_line_hex = add
         transmit_log_file.addTxData(wapice_test_line_hex,total_milliseconds)
         trdelay.append(total_milliseconds)
         lpwa_interface.transmit(wapice_test_line_hex)
    time.sleep(10)
    lpwa_interface.stop_gateway_logging()
    transmit_log_file.strore_data()




    transmitlog = transmit_log_file.read_file(transmit_log_file.transmitterFileName)

    transmit_log_file.return_csv_filename()

    print("testing delays:")
    delay, snr, rssi, cf, sf, per  = transmit_log_file.calculate_delays(trdelay)
    print("delay: ",delay)
    print("rssi: ", rssi)
    print("cf: ", cf)
    print("sf: ", sf)
    print("delay: ", snr)
    print("PER", per)
    #graafi = graph()
    #graafi.plot(transmissioncount, snr, delay, rssi, 'snr(dB)', 'delay (ms)','rssi(dBm)')
if __name__ == "__main__":
    main()