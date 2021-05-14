import requests
from bs4 import BeautifulSoup
import csv
import string
import pandas as pd
import lxml.html as lh
from pip._internal.utils.misc import enum

output = csv.writer(open('game_report.csv', 'w'))
# output.writerow(
#     ['Team', 'Name', 'Goals', 'Assists', 'SOG', 'Points', 'Power Play Points', 'Power Play Goals', 'Power Play Assists',
#      'Primary Points', 'Primary Power Play Points', 'Even-Strength Goals', 'Even-strength primary assists',
#      'Even-strength primary points'
#         , 'Short Handed Points', 'Short Handed Goals', 'Empty-Net Points'])

url = input("Enter the url of the game report: ")
result = requests.get(url)
src = result.content
soup = BeautifulSoup(src, 'html.parser')
table = soup.find_all("table")

# table[0] = top row table[1] = refs table[2] = game start/end table[3] = scoring box table[4] scoring box header
# table[5] = shots table[6] = pp,pim,pts  table[7] = v-h,#,per,Team,Time,Goals,Assist,Type,On-Ice+/-
# table[9] = team 1  roster, table[10] = team 1 goalies
# table[11] = team 2 roster, table[12] = team 2 goalies
# table[13] = Penalties

output.writerow(
    ['Team', 'Name', 'Goals', 'Assists', 'SOG', 'Points', 'Power Play Points', 'Power Play Goals', 'Power Play Assists',
     'Primary Points', 'Primary Power Play Points', 'Even-Strength Goals', 'Even-strength primary assists',
     'Even-strength primary points'
        , 'Short Handed Points', 'Short Handed Goals', 'Empty-Net Points'])

team1 = table[9].text
team2 = table[11].text
team2 = team2.splitlines()
team1 = team1.splitlines()
p1 = []
p2 = []
team1List = []
team2List = []

theDate = table[0].text.splitlines()
theDate[:] = [x for x in theDate if x]
theDate = theDate[2]
team1[:] = [x for x in team1 if x]
team2[:] = [x for x in team2 if x]
primeStats = table[7].text
primeStats = primeStats.splitlines()
primeStats[:] = [x for x in primeStats if x]
for i in range(9):
    primeStats.pop(0)

pStats = []
primeStatsList = []
for i in range(len(primeStats)):
    if i % 12 == 0 and i != 0 or i == len(primeStats) - 1:
        primeStatsList.append(pStats)
        pStats = []
        pStats.append(primeStats[i])
    else:
        pStats.append(primeStats[i])

# primeStats[0] = score pS[1] = goal num pS[2] = period pS[3] = Team ps[4] = Time ps[5] = Goal Scorer ps[6] = Assists from
# ps[7] = tpye ps[8-11] = doesnt matter
team1Name = team1.pop(0)
team1.pop(0)
for i in range(len(team1)):
    if i % 8 == 0 and i != 0:
        team1List.append(p1)
        p1 = []
        p1.append(team1[i])
    else:
        p1.append(team1[i])

team2Name = team2.pop(0)
team2.pop(0)
for i in range(len(team2)):
    if i % 8 == 0 and i != 0:
        team2List.append(p2)
        p2 = []
        p2.append(team2[i])
    else:
        p2.append(team2[i])

temp = [team1List, team2List]
for k in range(2):
    for player in temp[k][0:len(temp[k])]:
        if '\xa0' not in player:
            pos = player[0]
            num = player[1]
            name = player[2]
            goals = player[3]
            assists = player[4]
            plusminus = player[5]
            shots = player[6]
            penMin = player[7]
            ppGoals = 0
            ppAssists = 0
            ppPoints = 0
            primaryPoints = 0
            primaryPPPoints = 0
            evenStrengthPoints = 0
            evenStrengthGoals = 0
            evenStrengthAssists = 0
            evenStrengthPrimaryPoints = 0
            evenStrengthPrimaryAssists = 0
            emptyNetPoints = 0
            shortHandedPoints = 0
            shortHandedGoals = 0
            for i in range(len(primeStatsList)):
                # goals
                if name in primeStatsList[i][5] and primeStatsList[i][7] == 'PP':
                    ppGoals += 1
                    ppPoints += 1
                    primaryPoints += 1
                    primaryPPPoints += 1
                if name in primeStatsList[i][5] and primeStatsList[i][7] == 'SH':
                    shortHandedPoints += 1
                    shortHandedGoals += 1
                    primaryPoints += 1
                if name in primeStatsList[i][5] and primeStatsList[i][7] == '\xa0':
                    evenStrengthGoals += 1
                    evenStrengthPoints += 1
                    evenStrengthPrimaryPoints += 1
                    primaryPoints += 1
                if name in primeStatsList[i][5] and primeStatsList[i][7] == 'EN':
                    emptyNetPoints += 1

                # first assists
                assistsFrom = primeStatsList[i][6].split(',')
                if name in assistsFrom[0] and primeStatsList[i][7] == 'PP':
                    ppAssists += 1
                    primaryPoints += 1
                    primaryPPPoints += 1

                elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == 'PP':
                    ppAssists += 1

                if name in assistsFrom[0] and primeStatsList[i][7] == '\xa0':
                    evenStrengthAssists += 1
                    evenStrengthPoints += 1
                    evenStrengthPrimaryPoints += 1
                    evenStrengthPrimaryAssists += 1
                    primaryPoints += 1
                elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == '\xa0':
                    evenStrengthAssists += 1
                if name in assistsFrom[0] and primeStatsList[i][7] == 'EN':
                    emptyNetPoints += 1
                elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == 'EN':
                    emptyNetPoints += 1
                if name in assistsFrom[0] and primeStatsList[i][7] == 'SH':
                    shortHandedPoints += 1
                elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == 'SH':
                    shortHandedPoints += 1

        # 'Team','Name', 'Goals', 'Assists', 'SOG', 'Points', 'Power Play Points', 'Power Play Goals', 'Power Play Assists',
        #          'Primary Points', 'Primary Power Play Points', 'Even-Strength Goals', 'Even-strength primary assists', 'Even-strength primary points'
        #         ,'Short Handed Points','Short Handed Goals','Empty-Net Points'
        teamName = ' '
        if k == 0:
            teamName = team1Name
        else:
            teamName = team2Name
        output.writerow([teamName, name, goals, assists, shots, int(goals) + int(assists), ppPoints, ppGoals, ppAssists,
                         primaryPoints,
                         primaryPPPoints, evenStrengthGoals, evenStrengthPrimaryAssists, evenStrengthPrimaryPoints,
                         shortHandedPoints,
                         shortHandedGoals,
                         emptyNetPoints])

# teams = test.find_all("tr")
# for team in teams[1:len(teams)]:
#     stats = team.find_all("td")
#     name = stats[1].text
#     team = stats[2].text
#     gp = stats[3].text
#     g = stats[4].text
#     a = stats[5].text
#     tp = stats[6].text
#     ppg = stats[7].text
#     pim = stats[8].text
#     plus = stats[9].text
#     output.writerow([name,team, gp,g,a,tp,ppg,pim,plus])
#
# for player in team2List[0:len(team2List)]:
#     if '\xa0' not in player:
#         pos = player[0]
#         num = player[1]
#         name = player[2]
#         goals = player[3]
#         assists = player[4]
#         plusminus = player[5]
#         shots = player[6]
#         penMin = player[7]
#         ppGoals = 0
#         ppAssists = 0
#         ppPoints = 0
#         primaryPoints = 0
#         primaryPPPoints = 0
#         evenStrengthPoints = 0
#         evenStrengthGoals = 0
#         evenStrengthAssists = 0
#         evenStrengthPrimaryPoints = 0
#         evenStrengthPrimaryAssists = 0
#         emptyNetPoints = 0
#         shortHandedPoints = 0
#         shortHandedGoals = 0
#         for i in range(len(primeStatsList)):
#             # goals
#             if name in primeStatsList[i][5] and primeStatsList[i][7] == 'PP':
#                 ppGoals += 1
#                 ppPoints += 1
#                 primaryPoints += 1
#                 primaryPPPoints += 1
#             if name in primeStatsList[i][5] and primeStatsList[i][7] == 'SH':
#                 shortHandedPoints += 1
#                 shortHandedGoals += 1
#             if name in primeStatsList[i][5] and primeStatsList[i][7] == '':
#                 evenStrengthGoals += 1
#                 evenStrengthPoints += 1
#                 evenStrengthPrimaryPoints += 1
#             if name in primeStatsList[i][5] and primeStatsList[i][7] == 'EN':
#                 emptyNetPoints += 1
#
#             # first assists
#             assistsFrom = primeStatsList[i][6].split(',')
#             if name in assistsFrom[0] and primeStatsList[i][7] == 'PP':
#                 ppAssists += 1
#                 primaryPoints += 1
#                 primaryPPPoints += 1
#
#             elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == 'PP':
#                 ppAssists += 1
#
#             if name in assistsFrom[0] and primeStatsList[i][7] == '':
#                 evenStrengthAssists += 1
#                 evenStrengthPoints += 1
#                 evenStrengthPrimaryPoints += 1
#                 evenStrengthPrimaryAssists += 1
#             elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == '':
#                 evenStrengthAssists += 1
#             if name in assistsFrom[0] and primeStatsList[i][7] == 'EN':
#                 emptyNetPoints += 1
#             elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == 'EN':
#                 emptyNetPoints += 1
#             if name in assistsFrom[0] and primeStatsList[i][7] == 'SH':
#                 shortHandedPoints += 1
#             elif len(assistsFrom) > 1 and name in assistsFrom[1] and primeStatsList[i][7] == 'SH':
#                 shortHandedPoints += 1
#
#     # 'Team','Name', 'Goals', 'Assists', 'SOG', 'Points', 'Power Play Points', 'Power Play Goals', 'Power Play Assists',
#     #          'Primary Points', 'Primary Power Play Points', 'Even-Strength Goals', 'Even-strength primary assists', 'Even-strength primary points'
#     #         ,'Short Handed Points','Short Handed Goals','Empty-Net Points'
#
#     output.writerow(
#         [team2Name, name, goals, assists, shots, int(goals) + int(assists), ppPoints, ppGoals, ppAssists,
#          primaryPoints,
#          primaryPPPoints, evenStrengthGoals, evenStrengthPrimaryAssists, evenStrengthPrimaryPoints,
#          shortHandedPoints,
#          shortHandedGoals,
#          emptyNetPoints])
