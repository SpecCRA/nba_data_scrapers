import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://www.basketball-reference.com/leagues/NBA_2017_advanced.html"
r = requests.get(url)
soup = BeautifulSoup(r.text)

f = open("16_17_player_stats_advanced.html", "w")
f.write(r.text)
