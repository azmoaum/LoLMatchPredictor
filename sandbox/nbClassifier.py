from sklearn.naive_bayes import GaussianNB, MultinomialNB
import json

f = open("testInput.json")
rawData = json.load(f)
x = rawData.keys()


def dataAndClassification(start,stop):
	inputData = []
	result = [] 
	for i in range(start,stop):
		key = x[i]
		if rawData[key]["team1Win"] == True:
			for j in range(0,5):
				rawData[key]["team1"][j]["win"] = True
				rawData[key]["team2"][j]["win"] = False
		else:
			for j in range(0,5):
				rawData[key]["team1"][j]["win"] = False
				rawData[key]["team2"][j]["win"] = True
		players = rawData[key]["team1"] + rawData[key]["team2"]
		for player in players:
			if player["championGamesPlayed"] !=0:
				inputData.append([
					player["championMasteryLevel"],
					player["championGamesPlayed"],
					player["championWinrate"],
					player["totalMasteryPoints"],
					player["championDamageDealt"],
					player["championMasteryPoints"],
					player["championGoldEarned"]/player["championGamesPlayed"],
					player["championId"],
					player["summonerId"],
					player["totalMasteryLevel"],
					player["championKDA"]
				])
			else:
				inputData.append([
					player["championMasteryLevel"],
					player["championGamesPlayed"],
					player["championWinrate"],
					player["totalMasteryPoints"],
					player["championDamageDealt"],
					player["championMasteryPoints"],
					0,
					player["championId"],
					player["summonerId"],
					player["totalMasteryLevel"],
					player["championKDA"]
				])
			if player["win"]:
				result.append(1)
			else:
				result.append(0)
	return [inputData,result]


trainingData = dataAndClassification(0,len(x)/4)
data = trainingData[0]
classifications = trainingData[1]
testingData = dataAndClassification(len(x)/4,len(x))
testData = testingData[0]
testClassifications = testingData[1]
testResults= []

# Data attribute order:
#championMasteryLevel, championGamesPlayed, championWinrate, totalMasteryPoints, championDamageDealt, championMasteryPoints, championGoldEarned, totalMasteryLevel, championKDA

# classifications legend
# Won game = 1 Lost game = 0 

clf = GaussianNB()
clf = clf.fit(data, classifications)

for test in testData:
	testResults.append(clf.predict_proba([test]))
winChance = []
for test in testResults:
	winChance.append(test[0][1])

teamSplit = [winChance[i:i+5] for i in range(0,len(winChance), 5)]
teams = []
for i in range(0,len(teamSplit)):
	teamSplit[i].append((testClassifications[i*5]==1))
	teams.append(teamSplit[i])
finalresults = []

for team in teams:
	sumOfWinChance = 0
	ProductOfWinChance = 1
	for player in team[:-1]:
		sumOfWinChance = sumOfWinChance + player
		ProductOfWinChance = ProductOfWinChance * player
	finalresults.append([ProductOfWinChance, sumOfWinChance, team[-1]])
gameSplit = [teamSplit[i:i+2] for i in range(0,len(teamSplit), 2)]
sumOfWinChance = []

comparison= []
for i in range(0,len(finalresults)/2):
	comparison.append([finalresults[i*2][0]-finalresults[i*2+1][0],finalresults[i*2][1]-finalresults[i*2+1][1],finalresults[i*2][2]])

print comparison
different = 0
working = []
workingProduct = []
for thing in comparison:
	workingProduct
	working.append((thing[0]>0 and thing[2]) or (thing[0]<0 and (not thing[2])))
correct = 0
for thing in working:
	if thing:
		correct = correct + 1
print `correct` + "/" + `len(working)`
print working



i = 0
while i<(len(testResults)-10):
	sumOfWinChance = 0
	ProductOfWinChance = 1
	k = 0
	for j in range (i,i+5):
		k=j
		sumOfWinChance = sumOfWinChance + testResults[j][0][1]
		ProductOfWinChance = ProductOfWinChance * testResults[j][0][1]
	i = k + 1
	# print "sumOfWinChance: " + `sumOfWinChance`
	# print "ProductOfWinChance: " + `ProductOfWinChance`
	# print testClassifications[i-2]
	# print "\n\n"



# print testResults[i]
# print testClassifications[i]
# print "\n"
