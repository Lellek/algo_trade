# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 22:34:38 2021

@author: Leon
"""
from base import save_obj
from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table', attrs={'id':'constituents'})
rows = table.find_all("tr")

sandptickers = []

for row in rows:
    try:
        ticker = str(row.find("td").find("a").contents[0])
        if("-" in ticker):
            print(ticker)
        else:
            sandptickers.append(ticker)
        
    except:
        pass
    
save_obj(sandptickers, "SandP-Companies_Tickers")
