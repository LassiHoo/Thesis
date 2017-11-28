from EndNodeInitialization import loraWanPlatfom
from EndNodeInitialization import basePlatform
from EndNodeInterface import LoraWan
import sys

def main():
    transmitSettings = basePlatform()
    endnodeInterFace = LoraWan()
    endnodeInterFace.initInterface()

    for i in transmitSettings.sendCount:
        sleep (transmitSettings.sendInterval)
        endnodeInterFace.transmit("testi")


if __name__ == "__main__":
    main()