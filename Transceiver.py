from BasePlatform import basePlatform
from Lorawan import LoraWan
from file_handler import file_hander
import os
import datetime
import random
import time
import binascii
import threading
#from Graph import graph
pi = 0
def transmit_thread_function(transmit_settings,lpwa_interface):

    print("thread started transmitter settings ")
    if (transmit_settings[0]['start_time'] == 'dummy'):
        print("dummy detected")
    else:
        pi = 0
        dec = 0
        if (transmit_settings[0]['send_forever']=='true'):
            while True:
                if 2* transmit_settings[0]['interval_decrement_milliseconds'] >= (transmit_settings[0]['send_interval_milliseconds'] - dec ):
                    pi = 0
                    dec = 0
                print("running forever in thread")
                dec = transmit(transmit_settings, pi, lpwa_interface)
                print("dec: ", dec, " send interval: ", transmit_settings[0]['send_interval_milliseconds'])
                pi = pi + 1


        else:
            for i in range(0, transmit_settings[0]['send_count']):
                print("running in thread, transmission counts left" , ( transmit_settings[0]['send_count'] - i ) )
                transmit(transmit_settings, i ,lpwa_interface)


def transmit(transmit_settings, pi, lpwa_interface):

    dec = int(pi)*transmit_settings[0]['interval_decrement_milliseconds']
    sleep_time = (transmit_settings[0]['send_interval_milliseconds'] - dec)/1000.0
    #sleep_time = (transmit_settings.sendInterval/1000.0)
    print("sleep time: ",sleep_time)
    time.sleep(sleep_time)
    date = datetime.datetime.utcnow()
    total_milliseconds = ( date.microsecond / 1000) + ( date.minute * 60 * 1000 ) + (date.second * 1000)
    print("date in dec ", total_milliseconds)
    #datemilliseocndhex = hex( total_milliseconds)[2:]
    frame = str(total_milliseconds) + ":" + str(pi) + ":" + str(sleep_time)
    #print("date in hex ", datemilliseocndhex)
    frame_hex = binascii.hexlify(frame)
    add = hex(random.randint(0,20))[2:]
    wapice_test_line_hex = add
    #transmit_log_file.addTxData(wapice_test_line_hex,total_milliseconds)
    #trdelay.append(total_milliseconds)
    if transmit_settings[0]['data_content'] == 'from_diagnostic_frame':
        lpwa_interface.transmit(frame_hex)
    else:
        lpwa_interface.transmit(add)
    return dec

def main():

    transmit_settings = basePlatform()
    lpwa_interface = LoraWan()
    lpwa_interface.initInterface()
    threads = [threading.Thread(target=transmit_thread_function, args=[transmit_settings.data[f],lpwa_interface]) for f in transmit_settings.data]
    for thread in threads:
        print(" Starting transmitter thread: ", thread.getName() )
        thread.daemon
        thread.start()

if __name__ == "__main__":
    main()