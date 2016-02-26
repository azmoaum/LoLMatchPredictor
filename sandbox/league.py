#!/usr/bin/env python

import sys
import numpy as np
from sklearn import tree

# Contains the available data for one match when testing a classifier.
# Each team (Won / Lost) has 5 players
class Match():
  def __init__(self, matchId, matchDuration, queueType, mapId):
    # Map data
    self.matchId = matchId
    self.matchDuration = matchDuration
    self.queueType = queueType
    self.mapId = mapId

    # Player data - each list contains 5 Player classes
    self.team1 = []
    self.team2 = []

  def __str__(self):
    s = 'Match ' + str(self.matchId) + ' lasted for '
    s += str(int(self.matchDuration / 60)) + 'm ' + str(int(self.matchDuration % 60)) + 's'
    return s

# Contains data player data for a single game
class Player():
  def __init__(self, participantId,	championId,	spell1Id,	spell2Id,	highestAchievedSeasonTier,
               winner, kills, deaths, assists, totalDamageDealtToChampions, wardsPlaced,
               wardsKilled, inhibitorKills, towerKills, summonerId, matchHistoryUrl):
    self.participantId = participantId  # player number (= any int value from 1 to 10)
    self.championId = championId
    self.spell1Id = spell1Id            # first summoner spell id
    self.spell2Id = spell2Id            # second summoner spell id

    rankInt = 0
    if (highestAchievedSeasonTier == 'UNRANKED'):
      rankInt = 0
    elif (highestAchievedSeasonTier == 'BRONZE'):
      rankInt = 1
    elif (highestAchievedSeasonTier == 'SILVER'):
      rankInt = 2
    elif (highestAchievedSeasonTier == 'GOLD'):
      rankInt = 3
    elif (highestAchievedSeasonTier == 'PLATINUM'):
      rankInt = 4
    elif (highestAchievedSeasonTier == 'DIAMOND'):
      rankInt = 5
    elif (highestAchievedSeasonTier == 'MASTER'):
      rankInt = 6
    elif (highestAchievedSeasonTier == 'CHALLENGER'):
      rankInt = 7
    else:
      print 'ERROR: highestAchievedSeasontTier has an invalid value of: ',
      print str(highestAchievedSeasonTier)
      sys.exit()
    self.highestAchievedSeasonTier = rankInt  # Highest rank achieved (converted to int value)

    self.winner = winner    # true if the player won this game
    self.kills = kills
    self.deaths = deaths
    self.assists = assists
    self.totalDamageDealtToChampions = totalDamageDealtToChampions
    self.wardsPlaced = wardsPlaced
    self.wardsKilled = wardsKilled
    self.inhibitorKills = inhibitorKills
    self.towerKills = towerKills
    self.summonerId = summonerId
    self.matchHistoryUrl = matchHistoryUrl

  @classmethod
  def tmpConstructor(self, kills, deaths, assists):
    return Player(0,0,0,0,'UNRANKED',0,kills, deaths, assists, 0,0,0,0,0,0,0)

  def __str__(self):
    s = 'Summoner ' + str(self.summonerId)
    s += ' played champion ' + str(self.championId)
    s += ' with a score of ' + str(self.kills) + '/' + str(self.deaths) + '/' + str(self.assists)
    return s


# Puts the data from test.csv into the players list and matches list
def getDataFromCSV(players, matches):
  print 'Reading data from test.csv'

  # mydata = np.recfromcsv('test.csv', delimiter=',');
  mydata = np.recfromcsv('test.csv', delimiter=',', filling_values=np.nan, case_sensitive=True,
                         deletechars='', replace_space=' ')

  pid = 'participantId'
  cid = 'championId'
  sid1 = 'spell1Id'
  sid2 = 'spell2Id'
  rank = 'highestAchievedSeasonTier'
  win = 'winner'
  kills = 'kills'
  deaths = 'deaths'
  assists = 'assists'
  dmg = 'totalDamageDealtToChampions'
  wp = 'wardsPlaced'
  wk = 'wardsKilled'
  ik = 'inhibitorKills'
  tk = 'towerKills'
  sumid = 'summonerId'
  url = 'matchHistoryUri'

  for oneGame in mydata:
    m = Match(oneGame['matchId'], oneGame['matchDuration'], oneGame['queueType'], oneGame['mapId'])

    # Add all player data to players list (training data)
    for i in range(1, 11):
      p = Player(oneGame[pid + str(i)], oneGame[cid + str(i)], oneGame[sid1 + str(i)],
                 oneGame[sid2 + str(i)], oneGame[rank + str(i)], oneGame[win + str(i)],
                 oneGame[kills + str(i)], oneGame[deaths + str(i)],
                 oneGame[assists + str(i)], oneGame[dmg + str(i)], oneGame[wp + str(i)],
                 oneGame[wk + str(i)], oneGame[ik + str(i)], oneGame[tk + str(i)],
                 oneGame[sumid + str(i)], oneGame[url + str(i)])

      players.append(p)

      if (p.winner):
        m.team1.append(p)
      else:
        m.team2.append(p)

    matches.append(m)

# Add training data
def addDataToClf(data, result, players):
  for p in players:
    data.append((p.kills, p.deaths, p.assists))
    result.append((p.winner))

# Splits list l into n size lists
def splitList(l, n):
  return [l[x : x + n] for x in xrange(0, len(l), n)]

# Uses random forests (5 simple decision trees - 1 for each player)
def DecisionTreeClassifer1(players, matches):
  data = []     # Contains data we are making decisions on
  result = []   # True if team won and false if team lost

  matches = splitList(matches, 200) # split matches into lists of size 200

  # Currently only uses first 200 matches as training data
  for m in matches[0]:
    addDataToClf(data, result, m.team1)
    addDataToClf(data, result, m.team2)

  clf = tree.DecisionTreeClassifier()
  clf = clf.fit(data, result)

  correct = 0
  numCases = 0
  for m in matches[1]:
    teams = [m.team1, m.team2]
    for t in teams:
      numCases += 1
      countWins = 0
      for p in t:
        onePrediction = clf.predict([[p.kills,p.deaths,p.assists]])
        # print p.kills, p.deaths, p.assists, ' - ', onePrediction[0]
        if(onePrediction[0]):
          countWins += 1

      # If more than 2 of the decision trees predict win
      if (countWins > 2):
        if (t[0].winner):
          # print 'Predict win and team won'
          correct += 1
        else:
          # print 'Predict win and team lost'
          pass
      else:
        if (t[0].winner):
          # print 'Predict lose and team win'
          pass
        else:
          # print 'Predict lose and team lost'
          correct += 1

  print 'Random forest accuracy: ', (100.0 * correct / numCases), '%'


if __name__ == '__main__':
  players = []  # Contains list of Player classes from csv
  matches = []  # Contains list of Match classes from csv
  getDataFromCSV(players, matches)

  print 'Printing 4 players'
  for i in range (0, 4):
    print players[i]

  print 'Printing 2 matches'
  for i in range (0, 2):
    print matches[i]

  DecisionTreeClassifer1(players, matches)
