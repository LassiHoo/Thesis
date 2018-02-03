from BasePlatform import basePlatform
from Lorawan import LoraWan
from file_handler import file_hander
import os
import datetime
import random
import time
import binascii
import threading
from Graph import graph
pi = 0
def transmit_thread_function(transmit_settings,lpwa_interface):


    print("thread started transmitter settings ", transmit_settings)
    print(transmit_settings)
    #if (transmit_settings[0]['start_time'] == 'dummy'):
    #    print("dummy detected")
    pi = 0
    # while True:
    #
    #      dec = (int(pi)*transmit_settings.return_transmit_settings('interval_decrement_milliseconds'))
    #      if dec > transmit_settings.return_transmit_settings('send_interval_milliseconds'):
    #          pi = 0
    #          dec = 0
    #      sleep_time = transmit_settings.return_transmit_settings('send_interval_milliseconds' - dec)/1000.0
    #      #sleep_time = (transmit_settings.sendInterval/1000.0)
    #      print("sleep time: ",sleep_time)
    #      time.sleep(sleep_time)
    #      date = datetime.datetime.utcnow()
    #      total_milliseconds = ( date.microsecond / 1000) + ( date.minute * 60 * 1000 ) + (date.second * 1000)
    #      print("date in dec ", total_milliseconds)
    #      #datemilliseocndhex = hex( total_milliseconds)[2:]
    #      frame = str(total_milliseconds) + ":" + str(pi) + ":" + str(sleep_time)
    #      #print("date in hex ", datemilliseocndhex)
    #      frame_hex = binascii.hexlify(frame)
    #      add = hex(random.randint(0,20))[2:]
    #      wapice_test_line_hex = add
    #      #transmit_log_file.addTxData(wapice_test_line_hex,total_milliseconds)
    #      #trdelay.append(total_milliseconds)
    #      if transmit_settings.return_transmit_settings('data_content') == 'from_diagnostic_frame':
    #          lpwa_interface.transmit(frame_hex)
    #
    #      pi = pi + 1


def main():

    transmit_settings = basePlatform()
    lpwa_interface = LoraWan()
    lpwa_interface.initInterface()
    threads = [threading.Thread(target=transmit_thread_function, args=[transmit_settings.data[0][f],lpwa_interface]) for f in transmit_settings.data]
    for thread in threads:
        print(" Starting transmitter thread: ", thread.getName() )
        thread.start()

if __name__ == "__main__":
    main()