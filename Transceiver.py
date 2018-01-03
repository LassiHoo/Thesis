from BasePlatform import basePlatform
from Lorawan import LoraWan

import time

def main():

    transmit_settings = basePlatform()
    lpwa_interface = LoraWan()
    lpwa_interface.initInterface()
    #lpwa_interface.start_gateway_logging()



    for i in range (0,transmit_settings.sendCount):
         time.sleep(3)
         lpwa_interface.transmit("dsfhlksdf")


if __name__ == "__main__":
    main()