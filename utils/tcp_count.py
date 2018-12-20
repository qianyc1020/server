import re


class TcpCount(object):

    def get_contents(self, file):
        f = open(file, "r").readlines()
        return f

    def covert_number(self, number):
        value = hex(number)
        return value

    def get_connect(self, port):
        ESTABLISHED = []
        port = str(self.covert_number(port)).replace("0x", "").upper()
        for i in self.get_contents('/proc/net/tcp'):
            c = i.split()
            p = re.findall(r":.*%(port)s" % vars(), c[1])

            if c[3] == "01" and p:
                ESTABLISHED.append(c[3])
        return len(ESTABLISHED)

    def get_info(self, port1):
        ESTABLISHED = []
        SYN_SENT = []
        SYN_RECV = []
        FIN_WAIT1 = []
        FIN_WAIT2 = []
        TIME_WAIT = []
        CLOSE = []
        CLOSE_WAIT = []
        CLOSING = []
        port = str(self.covert_number(port1)).replace("0x", "").upper()
        for i in self.get_contents('/proc/net/tcp'):
            c = i.split()
            p = re.findall(r":.*%(port)s" % vars(), c[1])

            if c[3] == "01" and p:
                ESTABLISHED.append(c[3])
            elif c[3] == "02" and p:
                SYN_SENT.append(c[3])
            elif c[3] == "03" and p:
                SYN_RECV.append(c[3])
            elif c[3] == '04' and p:
                FIN_WAIT1.append(c[3])
            elif c[3] == '05' and p:
                FIN_WAIT2.append(c[3])
            elif c[3] == '06' and p:
                TIME_WAIT.append(c[3])
            elif c[3] == '07' and p:
                CLOSE.append(c[3])
            elif c[3] == '08' and p:
                CLOSE_WAIT.append(c[3])
            elif c[3] == '0B' and p:
                CLOSING.append(c[3])

        return str(port1) + "ESTABLISHED:\t" + str(len(ESTABLISHED)) + " \nSYN_SENT:\t" + str(len(SYN_SENT)) + \
               "\nSYN_RECV:\t" + str(len(SYN_RECV)) + " \nFIN_WAIT1:\t" + str(len(FIN_WAIT1)) + \
               "\nFIN_WAIT2:\t" + str(len(FIN_WAIT2)) + " \nTIME_WAIT:\t" + str(len(TIME_WAIT)) + \
               "\nCLOSE:  \t" + str(len(CLOSE)) + " \nCLOSE_WAIT:\t" + str(len(CLOSE_WAIT)) + \
               "\nCLOSING:\t" + str(len(CLOSING))
