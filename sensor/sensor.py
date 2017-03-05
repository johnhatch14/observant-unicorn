#!/usr/bin/python3

import scapy.all
from scapy.all import Packet
from scapy.layers.dot11 import Dot11


class UnicornSensor():

    IFACE = 'wlan1' # Interface we are capturing packets on, must be in monitor mode!!!
    AP_LIST = []

    def capture(self):
        scapy.all.sniff(iface = self.IFACE, prn = self.packetHandler)

    def packetHandler(self, rawpacket: Packet):
        # Prints all packets captured
        if rawpacket.haslayer(Dot11):
            pktFields = rawpacket.payload.fields

            if pktFields.type == 0 and pktFields.subtype == 8: # Beacon
                print(pktFields.addr)

    def event_HeardProbe(self, mac):

    def event_AccessPointHeard(self, station):


def main():
    print("Hello World! We come in peace, bringing Soylent...")
    UnicornSensor().capture()

if __name__ == '__main__':
    main()
