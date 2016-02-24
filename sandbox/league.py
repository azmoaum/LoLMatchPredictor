#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import random

class MyLeagueClassifer():

  def __init__(self):
    pass

  def fit(self):
    pass

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

if __name__ == '__main__':
  print "start"

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

  players = []

  # Add all player data to players list
  for oneGame in mydata:
    for i in range(1, 11):
      players.append(Player(oneGame[pid + str(i)], oneGame[cid + str(i)], oneGame[sid1 + str(i)],
                            oneGame[sid2 + str(i)], oneGame[rank + str(i)], oneGame[win + str(i)],
                            oneGame[kills + str(i)], oneGame[deaths + str(i)],
                            oneGame[assists + str(i)], oneGame[dmg + str(i)], oneGame[wp + str(i)],
                            oneGame[wk + str(i)], oneGame[ik + str(i)], oneGame[tk + str(i)],
                            oneGame[sumid + str(i)], oneGame[url + str(i)]))

  c1 = MyLeagueClassifer()
  c1.fit()
