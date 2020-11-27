import os
import scapy
from scapy.all import *
from scapy.layers.http import *
import pandas as pd

def extract_url_from_packets():
    packets = rdpcap("polarproxy.pcap")
    urls = pd.DataFrame(columns = ["URL"])    
    load_layer("http")

    for packet in packets:
        if packet.haslayer('HTTP'):
            txt=packet.show(dump=True)

        if packet.haslayer(HTTPRequest):
            if packet[HTTPRequest].Referer: 
                urls = urls.append({
                                        "URL": packet[HTTPRequest].Referer.decode(),
                                        "src": packet[IP].src,
                                        "dst": packet[IP].dst
                                    }, ignore_index=True)

    urls = urls.drop_duplicates(["URL"])
    urls = urls.reset_index(drop=True)

    return urls

if __name__ == "__main__":
    urls = extract_url_from_packets()
    print(urls["URL"])
    print(urls["src"])
    print(urls["dst"])