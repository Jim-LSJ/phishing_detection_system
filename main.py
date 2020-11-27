from extract_url import extract_url_from_packets
from collect_data import browse, create_driver, close_driver
from feature_extractor import parse_html
from model import lgbm_pred, load_model
from onos_rule import create_rule

import csv, os, sys
import pandas as pd
import numpy as np



def main():
    try:
        os.makedirs(os.path.join("screenshot"))
    except:
        pass

    # Load pre-trained LightGBM model
    gbm = load_model()

    while True:
        tuple_list = []
        # Waiting for polarproxy.pcap or Sniff packet (real time)
        print("\rWaiting for pcap files...", end="")

        # Extract urls from packet
        if "polarproxy.pcap" in os.listdir("."):
            print("\nExtract URLs...")
            urls = extract_url_from_packets()
            os.system("rm polarproxy.pcap")
        else:
            continue
            
        # # Extract urls from packet
        # print("Extract URLs...")
        
        # advance: using thread
        print("Create one driver")
        driver = create_driver()
        for i in range(len(urls)):
            url = urls.loc[i, "URL"]

            # Browse urls using Selenium, collect cookies (store in df), and return html
            df, html = browse(url, driver)
            if html is None:
                continue

            # Extract features from html and store in df
            df = parse_html(df, html)

            if df.loc[0, "input"] == 0 and df.loc[0, "iframe"] == 0:
                continue

            # Predict through LightGBM model
            pred_y = lgbm_pred(df, gbm)
            print("Prediction: {}".format("phishing" if pred_y[0] else "benign"))

            # Append suspect tuple to a list
            if pred_y[0] == 1:
                tuple_list.append( (urls.loc[i, "src"], urls.loc[i, "dst"]) )
        
        # Apply rules
        for t in tuple_list:
            create_rule(t[0], t[1])

        # Close driver
        close_driver(driver)

if __name__ == '__main__':
    main()

# Usage: python3 code/main.py