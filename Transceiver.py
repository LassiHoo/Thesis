from BasePlatform import loraWanPlatfom
from BasePlatform import basePlatform
from Lorawan import LoraWan
from SSH import ssh_connection
import sys

def main():
    ssh = ssh_connection()
    transmitSettings = basePlatform()
    endnodeInterFace = LoraWan()
    endnodeInterFace.initInterface()

    #log in to gateway
    ssh.Login()

    for i in range (0,transmitSettings.sendCount):
        sleep (transmitSettings.sendInterval)
        endnodeInterFace.transmit("testi")


if __name__ == "__main__":
    main()