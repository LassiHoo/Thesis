from pexpect import pxssh

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
            self.connection.sendline('tcpdump -w ' + filename)
        except pxssh.ExceptionPxssh as e:
            print("start tcp dump failed.")
            print(e)

    def GetTCPdumpFile(self, username, filename,localhost):
        try:
            self.connection.sendline('scp .' + username + '@' + localhost)
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on fet tcp dump file.")
            print(e)

# We can also execute multiple command like this:
#s.sendline('uptime;df -h')