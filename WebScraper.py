import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import lxml.html as lh

output = csv.writer(open('test_table.csv', 'w'))
output.writerow(['Name', 'Team', 'GP','G','A','TP','PPG','+/-'])
# output.writerow(['Team', 'Att', 'CMP', 'CMP%', 'YRDS/ATT',
#                  'Pass Yards', 'TD', 'INT', 'RATE', '1st', '1st%'])  # , '20', '40', 'LNG', 'SCK', 'SCKY'])
url = "https://www.eliteprospects.com/league/ahl/stats/2020-2021"
result = requests.get(url)
src = result.content
soup = BeautifulSoup(src, 'html.parser')
table = soup.find_all("table")

test = table[1]
teams = test.find_all("tr")
for team in teams[1:len(teams)]:
    stats = team.find_all("td")
    name = stats[1].text
    team = stats[2].text
    gp = stats[3].text
    g = stats[4].text
    a = stats[5].text
    tp = stats[6].text
    ppg = stats[7].text
    pim = stats[8].text
    plus = stats[9].text
    output.writerow([name,team, gp,g,a,tp,ppg,pim,plus])
