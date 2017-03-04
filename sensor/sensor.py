from scapy.all import *

class UnicornSensor():

    IFACE = 'wlan1' # Interface we are capturing packets on, must be in monitor mode!!!

    def main(self):
        print("Hello World! We come in peace, bringing Soylent...")
        sniff(iface = self.IFACE, prn = self.PacketHandler)

    def PacketHandler(self, pkt: Packet) :
        # Prints all packets captured
        print (pkt)

if __name__ == '__main__':
    UnicornSensor().main()