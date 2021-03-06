from BasePlatform import basePlatform
from Lorawan import LoraWan
import datetime
import random
import time
import binascii
import threading

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

def update_thread_list(transmit_settings):
    while 1:
        print("updating transmit Json data")
        transmit_settings.reload_Json_data()
        time.sleep(60)


def transmit(transmit_settings, pi, lpwa_interface):

    dec = int(pi)*transmit_settings[0]['interval_decrement_milliseconds']
    sleep_time = (transmit_settings[0]['send_interval_milliseconds'] - dec)/1000.0
    print("sleep time: ",sleep_time)
    time.sleep(sleep_time)
    date = datetime.datetime.utcnow()
    total_milliseconds = ( date.microsecond / 1000) + ( date.minute * 60 * 1000 ) + (date.second * 1000)
    print("date in dec ", total_milliseconds)
    frame = str(total_milliseconds) + ":" + str(pi) + ":" + str(sleep_time)
    frame_hex = binascii.hexlify(frame)
    add = hex(random.randint(0,20))[2:]

    if transmit_settings[0]['data_content'] == 'from_diagnostic_frame':
        lpwa_interface.transmit(frame_hex)
    else:
        lpwa_interface.transmit(add)
    return dec

def main():


    transmit_settings = basePlatform()
    lpwa_interface = LoraWan()
    lpwa_interface.initInterface()

    update_transmit_thread = threading.Thread(target=update_thread_list, args=[transmit_settings])
    update_transmit_thread.daemon
    update_transmit_thread.start()

    while True:
        time.sleep(1)
        for f in transmit_settings.data:
            if ( time.time() > transmit_settings.data[f][0]['start_time'] ) and ( transmit_settings.data[f][0]['status'] == 'waitin_to_start'):
                thread_start = threading.Thread(target=transmit_thread_function, args=[transmit_settings.data[f], lpwa_interface])
                print(" Starting transmitter thread: ", thread_start.getName())
                print("start time: ", transmit_settings.data[f][0]['start_time'])
                transmit_settings.data[f][0]['status'] = 'on'
                transmit_settings.store_Json_data()
                thread_start.daemon
                thread_start.start()

if __name__ == "__main__":
    main()