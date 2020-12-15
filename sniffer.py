import pandas as pd
import os, time, json
import threading

import scapy
from scapy.all import *
from scapy.layers import *

class flow_split_thread(threading.Thread):
    def __init__(self, session_time):
        threading.Thread.__init__(self)
        self.session_time=session_time
        self.urls = pd.DataFrame(columns = ["URL", "src", "dst"])

    def extract_url_from_packets(self, packets):
        load_layer("http")

        for packet in packets:
            if packet.haslayer(HTTPRequest):
                if packet[HTTPRequest].Referer:
                    print(packet[HTTPRequest].Referer.decode(), packet[IP].src, packet[IP].dst) 
                    self.urls = self.urls.append({
                                                    "URL": packet[HTTPRequest].Referer.decode(),
                                                    "src": packet[IP].src,
                                                    "dst": packet[IP].dst
                                                }, ignore_index=True)

        self.urls = self.urls.drop_duplicates(["URL"])
        self.urls = self.urls.reset_index(drop=True)

    def run(self):
        nic = "-"
        while True:
            sniff(prn=self.extract_url_from_packets, iface=nic, timeout=self.session_time)
            self.urls.to_csv(os.path.join("URLs", str(int(time.time())) + ".csv"), index=False)
            self.urls = pd.DataFrame(columns = ["URL", "src", "dst"])

def sniffing():
    # start sniffering thread
    session_time = 10
    thread1 = flow_split_thread(session_time)
    thread2 = flow_split_thread(session_time)
    
    thread1.start()
    time.sleep(5)
    thread2.start()

if __name__=="__main__":
    sniffing()