from pexpect import pxssh
import os
class ssh_connection:

    def __init__(self, ):

        self.connection = pxssh.pxssh()

    def Login(self, localhost, username, password):

        try:
            print("Login progress to ", localhost)
            print("username ", username)
            print("password ", password)
            self.connection.login(localhost, username, password)

        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)

    def StartTCPdump(self, filename):
        try:
            self.connection.sendline('sudo ./enableWriteAccess.sh')
            self.connection.sendline('cd github/lora_gateway/util_pkt_logger/')
            self.connection.sendline('sudo ./util_pkt_logger')
        except pxssh.ExceptionPxssh as e:
            print("start tcp dump failed.")
            print(e)

    def StopTCPdump(self):
        try:
            self.connection.sendline("\x03")
        except pxssh.ExceptionPxssh as e:
            print("stop tcp dump failed.")
            print(e)

    def GetTCPdumpFile(self, username, filename,localhost):
        try:
            scp = 'sshpass -p "raspberry" '+' scp '+ username + '@' + localhost + ":" + 'github/lora_gateway/util_pkt_logger/' + "\*.csv " + "."
            print(scp)
            os.system(scp)
            self.connection.sendline('sudo rm github/lora_gateway/util_pkt_logger/\*.csv')
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on fet tcp dump file.")
            print(e)

    def CloseConnection(self):
        try:
            self.connection.close()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed to close the connection.")
            print(e)

# We can also execute multiple command like this:
#s.sendline('uptime;df -h')