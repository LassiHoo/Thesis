from BasePlatform import basePlatform
from Lorawan import LoraWan
from file_handler import file_hander
import os
import datetime

import time

def main():
    wapice_test_line_hex = "576170696365204c505741207465737420656e7669726f6e6d656e74"
    tcp_dump_file_name = "Wapice.dat"

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

    for i in range (0, transmit_settings.sendCount):
         time.sleep(transmit_settings.sendInterval)
         date = datetime.now()
         transmit_log_file.addTxData(wapice_test_line_hex,date.microseconds)
         lpwa_interface.transmit(wapice_test_line_hex)
    time.sleep(10)
    lpwa_interface.stop_gateway_logging()
    transmit_log_file.stroredata()

if __name__ == "__main__":
    main()