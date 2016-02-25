#!/usr/bin/env python

import sys
import numpy as np
from sklearn import tree

# Contains the available data for one match when testing a classifier.
# Each team (Won / Lost) has 5 players and for each player we can get championId and summonerId
class Match():
  def __init__(self, matchId, matchDuration, queueType, mapId):
    # Map data
    self.matchId = matchId
    self.matchDuration = matchDuration
    self.queueType = queueType
    self.mapId = mapId

    # Player data - each list is of size 5
    self.WonSummonerIds = []
    self.WonChampionIds = []
    self.LostSummonerIds = []
    self.LostChampionIds = []

  def __str__(self):
    s = 'Match ' + str(self.matchId) + ' lasted for '
    s += str(int(self.matchDuration / 60)) + 'm ' + str(int(self.matchDuration % 60)) + 's\n'
    s += 'Winning team summoner ids: ' + str(self.WonSummonerIds) + '.\n'
    s += 'Losing team summoner ids: ' + str(self.LostSummonerIds)
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
      players.append(Player(oneGame[pid + str(i)], oneGame[cid + str(i)], oneGame[sid1 + str(i)],
                            oneGame[sid2 + str(i)], oneGame[rank + str(i)], oneGame[win + str(i)],
                            oneGame[kills + str(i)], oneGame[deaths + str(i)],
                            oneGame[assists + str(i)], oneGame[dmg + str(i)], oneGame[wp + str(i)],
                            oneGame[wk + str(i)], oneGame[ik + str(i)], oneGame[tk + str(i)],
                            oneGame[sumid + str(i)], oneGame[url + str(i)]))


      if (oneGame[win + str(i)] == True):
        m.WonChampionIds.append(oneGame[cid + str(i)])
        m.WonSummonerIds.append(oneGame[sumid + str(i)])
      else:
        m.LostChampionIds.append(oneGame[cid + str(i)])
        m.LostSummonerIds.append(oneGame[sumid + str(i)])

    matches.append(m)

def TestDecisionTreeClassifer():
  pass

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

  TestDecisionTreeClassifer()
