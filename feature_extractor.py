from bs4 import BeautifulSoup
import pandas as pd

def parse_html(df, html):
    html = BeautifulSoup(html, "html.parser")
    
    df.loc[0, "Tags"] = len(html.find_all())
    df.loc[0, "No-class Tags"] = len(html.find_all(class_=""))
    df.loc[0, "class Tags"] = df.loc[0, "Tags"] - df.loc[0, "No-class Tags"]
    df.loc[0, "div"] = len(html.find_all("div"))
    df.loc[0, "img"] = len(html.find_all("img"))
    df.loc[0, "iframe"] = len(html.find_all("iframe"))
    df.loc[0, "a"] = len(html.find_all("a"))
    df.loc[0, "form"] = len(html.find_all("form"))
    df.loc[0, "input"] = len(html.find_all("input"))
    df.loc[0, "script"] = len(html.find_all("script"))
    df.loc[0, "internal_script"] = len(html.find_all("script", src=""))
    df.loc[0, "external_script"] = df.loc[0, "script"] - df.loc[0, "internal_script"]
    
    print("Finish parse html")
    return df