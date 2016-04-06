#!/usr/bin/env python

import sys
import numpy as np
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import cross_validation

# Contains data about the match and each of the players in the game.
class Match():
  def __init__(self, matchId, matchDuration = None, queueType = None, mapId = None):
    # Map data
    self.matchId = matchId
    self.matchDuration = matchDuration  # length of match in seconds
    self.queueType = queueType          # type of queue (e.g. ranked solo, normals, etc.)
    self.mapId = mapId                  # type of map

    # Player data - each list contains 5 Player classes
    self.team1 = []
    self.team1Won = None

    self.team2 = []
    self.team2Won = None

  def __str__(self):
    s = 'Match ' + str(self.matchId)
    return s

# Contains data about a specific player
class Player():
  def __init__(self, summonerId, championId):
    # Current game stats
    self.summonerId = summonerId
    self.championId = championId

    self.participantId = None       # player number (= any int value from 1 to 10)
    self.spell1Id = None            # first summoner spell id
    self.spell2Id = None            # second summoner spell id

    # One completed game
    self.won = None
    self.kills = None
    self.deaths = None
    self.assists = None
    self.totalDamageDealtToChampions = None
    self.wardsPlaced = None
    self.wardsKilled = None
    self.inhibitorKills = None
    self.towerKills = None
    self.matchHistoryUrl = None

    # Champ history
    self.kda = None
    self.winrate = None
    self.mlvl = None

    # Player history
    self.highestAchievedSeasonTier = None  # Highest rank achieved

  # Add stats for the player from a completed game
  def addTestingGameData(self, participantId,	spell1Id,	spell2Id, highestAchievedSeasonTier, won,
                         kills, deaths, assists, totalDamageDealtToChampions, wardsPlaced,
                         wardsKilled, inhibitorKills, towerKills, matchHistoryUrl):
    self.participantId = participantId
    self.spell1Id = spell1Id
    self.spell2Id = spell2Id

    rankInt = None  # Default is None which means unknown rank
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
    self.highestAchievedSeasonTier = rankInt

    self.won = won
    self.kills = kills
    self.deaths = deaths
    self.assists = assists
    self.totalDamageDealtToChampions = totalDamageDealtToChampions
    self.wardsPlaced = wardsPlaced
    self.wardsKilled = wardsKilled
    self.inhibitorKills = inhibitorKills
    self.towerKills = towerKills
    self.matchHistoryUrl = matchHistoryUrl

  # Add stats based on the player's history
  def addTrainingGameData(self, kda, winrate, mlvl):
    self.kda = kda
    self.winrate = winrate
    self.mlvl = mlvl

  def __str__(self):
    s = 'Summoner ' + str(self.summonerId)
    s += ' played champion ' + str(self.championId)
    return s


# Takes the data from matches.csv and converts it into a list of matches
def getCurrentGameDataFromCSV(matches):
  print 'Reading data from matches.csv'

  # mydata = np.recfromcsv('matches.csv', delimiter=',');
  mydata = np.recfromcsv('matches.csv', delimiter=',', filling_values=np.nan, case_sensitive=True,
                         deletechars='', replace_space=' ')
  sumid = 'summonerId'
  cid = 'championId'
  pid = 'participantId'
  sid1 = 'spell1Id'
  sid2 = 'spell2Id'
  rank = 'highestAchievedSeasonTier'
  won = 'winner'
  kills = 'kills'
  deaths = 'deaths'
  assists = 'assists'
  dmg = 'totalDamageDealtToChampions'
  wp = 'wardsPlaced'
  wk = 'wardsKilled'
  ik = 'inhibitorKills'
  tk = 'towerKills'
  url = 'matchHistoryUri'

  for oneGame in mydata:
    m = Match(oneGame['matchId'], oneGame['matchDuration'], oneGame['queueType'], oneGame['mapId'])

    # Add all player data to players list (training data)
    for i in range(1, 11):
      p = Player(oneGame[sumid + str(i)], oneGame[cid + str(i)])
      p.addTestingGameData(oneGame[pid + str(i)], oneGame[sid1 + str(i)], oneGame[sid2 + str(i)],
                           oneGame[rank + str(i)], oneGame[won + str(i)], oneGame[kills + str(i)],
                           oneGame[deaths + str(i)], oneGame[assists + str(i)],
                           oneGame[dmg + str(i)], oneGame[wp + str(i)], oneGame[wk + str(i)],
                           oneGame[ik + str(i)], oneGame[tk + str(i)], oneGame[url + str(i)])

      if (i <= 5):
        m.team1.append(p)
      else:
        m.team2.append(p)

    m.team1Won = m.team1[0].won
    m.team2Won = m.team2[0].won
    assert m.team1Won != m.team2Won, str('Both team 1 won and team 2 won for match ', m.matchId)
    matches[m.matchId] = m

  print 'Finished parsing data from matches.csv'


# Takes the data from ParticipantInfo.csv and converts it into a list of matches
def getDataFromParticipantInfoCSV(matches):
  print 'Reading data from ParticipantInfo.csv'

  mydata = np.recfromcsv('ParticipantInfo.csv', delimiter=',', filling_values=np.nan, case_sensitive=True,
                         deletechars='', replace_space=' ')
  
  sumid = 'summonerId'
  cid = 'championId'
  kda = 'kda'
  winrate = 'winrate'
  mlvl = 'masteryLevel'

  m = None  # Current match
  currParticipant = 10

  # Add all player data for each match
  # First 5 players are team 1, next 5 players are team 2
  for onePlayer in mydata:
    if (currParticipant == 10):
      currParticipant = 0

      if (m is not None):
        matches.append(m)

      m = Match(onePlayer['matchId'])

    p = Player(onePlayer[sumid], onePlayer[cid])
    p.addTrainingGameData(onePlayer[kda], onePlayer[winrate], onePlayer[mlvl])

    if (currParticipant < 5):
      m.team1.append(p)
    else:
      m.team2.append(p)

    currParticipant += 1

  print 'Finished parsing data from ParticipantInfo.csv'

# Add training data
def addDataToClf(data, result, players):
  for p in players:
    data.append((p.kills, p.deaths, p.assists))
    result.append((p.winner))

# Splits list l into n size lists
def splitList(l, n):
  return [l[x : x + n] for x in xrange(0, len(l), n)]

# Add training data
def addDataToClf1(data, results, players, win):
  data.append(calculateAttributes(players))
  results.append(win)


# Add training data - using both teams
def addDataToClf2(data, results, team1, team2, win):
  t1 = calculateAttributes(team1)
  t2 = calculateAttributes(team2)
  data.append([t1[0] - t2[0], t1[1] - t2[1], t1[2] - t2[2]])
  results.append(win)

# Returns a list of data used in classifier
def calculateAttributes(players):
  avgKDA = 0.0
  avgWinrate = 0.0
  avgMasteryLvl = 0.0

  for p in players:
    avgKDA += p.kda
    avgWinrate += p.winrate
    avgMasteryLvl += p.mlvl

  avgKDA /= 5.0
  avgWinrate /= 5.0
  avgMasteryLvl /= 5.0

  return [avgKDA, avgWinrate, avgMasteryLvl]

# Uses a decision tree based on KDA, Win rate, Mastery points
def DecisionTreeClassifer1(testingMatches, trainingMatches):
  data = []     # Contains data we are making decisions on - method 1
  results = []   # True if team won and false if team lost

  for i in range(0, len(trainingMatches)):
    m = trainingMatches[i]

    # Looks up result from testingMatches
    addDataToClf1(data, results, m.team1, testingMatches[m.matchId].team1Won)
    addDataToClf1(data, results, m.team2, testingMatches[m.matchId].team2Won)

  clf = tree.DecisionTreeClassifier()
  clf = clf.fit(data, results)

  # Cross validation - use each set as training/testing
  scores = cross_validation.cross_val_score(clf, data, results, cv=10)
  print 'accuracy with 10-fold cv:'
  print 'method 1 (looking at single team):', scores.mean()

  for i in range(0, len(trainingMatches)):
    m = trainingMatches[i]

    # Looks up result from testingMatches
    addDataToClf2(data, results, m.team1, m.team2, testingMatches[m.matchId].team1Won)
    addDataToClf2(data, results, m.team2, m.team1, testingMatches[m.matchId].team2Won)

  scores = cross_validation.cross_val_score(clf, data, results, cv=10)
  print 'method 1 (looking at both teams):', scores.mean()

  '''
  trainingMatches = splitList(trainingMatches, 100) # split matches into 9 lists of size 1000

  # Only using first set as training and rest as testing
  trainingSet = trainingMatches[0]
  testingSet = trainingMatches[1:]

  for i in range(0, len(trainingSet)):
    m = trainingSet[i]

    # Looks up result from testingMatches
    addDataToClf1(data, results, m.team1, testingMatches[m.matchId].team1Won)
    addDataToClf1(data, results, m.team2, testingMatches[m.matchId].team2Won)

  print data[0]
  clf = tree.DecisionTreeClassifier()
  clf = clf.fit(data, results)

  predictedResults = []

  for test in testingSet:
    for m in test:
      teams = [m.team1, m.team2]

      for t in teams:
        prediction = clf.predict([calculateAttributes(t)])
        predictedResults.append(prediction)

  trueResults = []
  for test in testingSet:
    for m in test:
      trueResults.append(testingMatches[m.matchId].team1Won)
      trueResults.append(testingMatches[m.matchId].team2Won)
  print 'accuracy: ', accuracy_score(trueResults, predictedResults)
  '''

if __name__ == '__main__':
  testingMatches = {}  # Contains dictionary of matches from matches.csv with results
  trainingMatches = [] # Contains list of matches from ParticipantInfo.csv were result is unknown

  getCurrentGameDataFromCSV(testingMatches)
  getDataFromParticipantInfoCSV(trainingMatches)

  DecisionTreeClassifer1(testingMatches, trainingMatches)
