#!/usr/bin/python3

from scapy.all import sniff
from scapy.all import Packet
from scapy.layers.dot11 import Dot11
import time

from config import Config

class UnicornSensor():

    ap_list = []
    devices = {}

    def capture(self):
        configuration = Config()
        configuration.loadConfig()
        print("Listening on", configuration.interface)
        sniff(iface = configuration.interface, prn = self.packetHandler)

    def packetHandler(self, rawpacket: Packet):

        if rawpacket.haslayer(Dot11): # Make sure it is a dot11 packet
            pkt_fields = rawpacket.payload.fields

            if pkt_fields['type'] == 0 and pkt_fields['subtype'] == 4:  # Probe Request
                self.event_HeardProbe(pkt_fields['addr2'])

            if pkt_fields['type'] == 0 and pkt_fields['subtype'] == 8:  # Beacon
                self.event_AccessPointHeard(pkt_fields['addr2'])

    def event_HeardProbe(self, mac):
        print("HeardProbe from: " + str(mac))
        self.devices[str(mac)] = str(time.time())

    def event_AccessPointHeard(self, mac):
        print("AccessPoint heard: " + str(mac))
        if mac not in ap_list:
            ap_list.append(mac)

def main():
    print("Hello World! We come in peace, bringing Soylent...")
    UnicornSensor().capture()

if __name__ == '__main__':
    main()
