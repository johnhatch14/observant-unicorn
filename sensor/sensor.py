#!/usr/bin/python3

from scapy.all import sniff
from scapy.all import Packet
from scapy.layers.dot11 import Dot11
import time

from config import Config
from config import remove_new_line

class UnicornSensor():

    ap_list = []
    devices = {}
    blacklist = []
    whitelist = []

    def capture(self):
        configuration = Config()
        configuration.loadConfig()
        # read blacklist and whitelist
        try:
            with open("blacklist", 'r') as blacklist_file:
                mac = blacklist_file.readline()
                while mac != '':
                    self.blacklist.append(remove_new_line(mac))
                    mac = blacklist_file.readline()
            with open("whitelist", 'r') as whitelist_file:
                mac = whitelist_file.readline()
                while mac != "":
                    self.whitelist.append(remove_new_line(mac))
                    mac = whitelist_file.readline()
        except FileNotFoundError as ex:
            print("Please create '" + ex.filename + "' file")
        print("Listening on", configuration.interface)
        sniff(iface = configuration.interface, prn = self.packetHandler)

    def packetHandler(self, rawpacket: Packet):

        if rawpacket.haslayer(Dot11): # Make sure it is a dot11 packet
            pkt_fields = rawpacket.payload.fields

            if pkt_fields['type'] == 0 and pkt_fields['subtype'] == 4:  # Probe Request
                self.event_HeardProbe(pkt_fields['addr2'])

            if pkt_fields['type'] == 0 and pkt_fields['subtype'] == 8:  # Beacon
                self.event_AccessPointHeard(pkt_fields['addr2'])

            if pkt_fields['type'] == 0 and pkt_fields['subtype'] == (0 or 2): # Association Request
                self.event_HeardAssociation(pkt_fields['addr1'], pkt_fields['addr2'])

    def event_HeardProbe(self, mac):
        print("HeardProbe from: " + str(mac))
        self.devices[str(mac)] = str(time.time())
        if str(mac) in self.blacklist:
            print("Blacklisted MAC address", str(mac), "detected!")

    def event_AccessPointHeard(self, mac):
        print("AccessPoint heard: " + str(mac))
        if mac not in self.ap_list:
            self.ap_list.append(mac)

    def event_HeardAssociation(self, mac1, mac2):
        print(str(mac2), "attempting to associate with", str(mac1))

def main():
    print("Hello World! We come in peace, bringing Soylent...")
    UnicornSensor().capture()

if __name__ == '__main__':
    main()
