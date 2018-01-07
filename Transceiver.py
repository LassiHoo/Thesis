from BasePlatform import basePlatform
from Lorawan import LoraWan

import time

def main():
    wapice_test_line_hex = "576170696365204c505741207465737420656e7669726f6e6d656e74"
    transmit_settings = basePlatform()
    lpwa_interface = LoraWan()
    lpwa_interface.initInterface()
    #lpwa_interface.start_gateway_logging()



    for i in range (0,transmit_settings.sendCount):
         time.sleep(transmit_settings.sendInterval)
         lpwa_interface.transmit(wapice_test_line_hex)


if __name__ == "__main__":
    main()