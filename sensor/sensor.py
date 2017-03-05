#!/usr/bin/python3

from scapy.all import sniff
from scapy.all import Packet
from scapy.layers.dot11 import Dot11
import time
import os
from config import Config
from config import remove_new_line
import json


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

            with open('devices.json', 'w') as of:
                of.write(json.dumps(self.devices))

    def event_HeardProbe(self, mac):
        print("HeardProbe from: " + str(mac))
        self.devices[str(mac)] = str(time.time())
        self.devices[mac] = {'time': time.time(), 'associated': None, 'sensor_id': "1", 'ap': 0}
        
        if str(mac) in self.blacklist:
            print("Blacklisted MAC address", str(mac), "detected!")

    def event_AccessPointHeard(self, mac):
        # print("AccessPoint heard: " + str(mac))
        self.devices[mac] = {'time': time.time(), 'associated': None, 'sensor_id': "1", 'ap': 1}
        if mac not in self.ap_list:
            self.ap_list.append(mac)

    def event_HeardAssociation(self, mac1, mac2):
        # print(str(mac2), "attempting to associate with", str(mac1))
        self.devices[mac1] = {'time': time.time(), 'associated': mac2, 'sensor_id': "1", 'ap': 0}

def main():
    print("Hello World! We come in peace, bringing Soylent...")
    sensor = UnicornSensor()
    pid = os.fork()
    if pid == 0:
        while True:
            time.sleep(1)
    else:
        sensor.capture()

if __name__ == '__main__':
    main()
