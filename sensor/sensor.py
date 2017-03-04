#!/usr/bin/python3

import scapy.all

class UnicornSensor():

    IFACE = 'wlan1' # Interface we are capturing packets on, must be in monitor mode!!!

    def capture(self):
        scapy.all.sniff(iface = self.IFACE, prn = self.packetHandler)

    def packetHandler(self, pkt: scapy.all.Packet) :
        # Prints all packets captured
        print(pkt)

def main():
    print("Hello World! We come in peace, bringing Soylent...")
    UnicornSensor().capture()

if __name__ == '__main__':
    main()
