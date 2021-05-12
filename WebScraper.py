import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import lxml.html as lh

output = csv.writer(open('test_table.csv', 'w'))
# output.writerow(['Pos', 'Team', 'GP', 'A', 'PTS', '+/-', 'PIM', 'SHG', 'Pt/G','PIMPG', 'SH', 'SOG', 'SOA', 'SOGW', 'SO%'])
output.writerow(['Team', 'Att', 'CMP', 'CMP%', 'YRDS/ATT',
                 'Pass Yards', 'TD', 'INT', 'RATE', '1st', '1st%'])  # , '20', '40', 'LNG', 'SCK', 'SCKY'])
url = "https://www.nfl.com/stats/team-stats/"
result = requests.get(url)
src = result.content
soup = BeautifulSoup(src, 'html.parser')
table = soup.find_all("table")
# rint(soup)
test = table[0]
teams = test.find_all("tr")
for team in teams[1:32]:
    stats = team.find_all("td")
    name = stats[0].text
    att = stats[1].text
    cmp = stats[2].text
    cmpP = stats[3].text
    ydsPerAtt = stats[4].text
    pYards = stats[5].text
    td = stats[6].text
    inter = stats[7].text
    rate = stats[8].text
    first = stats[9].text
    firstPer = stats[10].text
    output.writerow([name, att,cmp,cmpP, ydsPerAtt,pYards,td,inter,rate,first,firstPer])

