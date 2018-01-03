from BasePlatform import loraWanPlatfom
from BasePlatform import basePlatform
from Lorawan import LoraWan

import sys

def main():

    transmit_settings = basePlatform()
    lpwa_interface = LoraWan()
    lpwa_interface.initInterface()
    #lpwa_interface.start_gateway_logging()



    # for i in range (0,transmit_settings.sendCount):
    #     sleep (transmit_settings.sendInterval)
    #     lpwa_interface.transmit("testi")


if __name__ == "__main__":
    main()