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
            pkt_fields = rawpacket.payload.fields
            #print(pkt_fields)
            if pkt_fields['type'] == 0 and pkt_fields['subtype'] == 4: # Probe Request
                self.event_HeardProbe(pkt_fields['addr2'])

            if pkt_fields['type'] == 0 and pkt_fields['subtype'] == 8:  # Beacon
                self.event_AccessPointHeard(pkt_fields['addr2'])

    def event_HeardProbe(self, mac):
        print("HeardProbe from:" + str(mac))

    def event_AccessPointHeard(self, mac):
        print("AccessPoint heard:" + str(mac))

def main():
    print("Hello World! We come in peace, bringing Soylent...")
    UnicornSensor().capture()

if __name__ == '__main__':
    main()
