#!/usr/bin/python

import sys
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score


def formatData(data, participantInfo):
    X = [] #average KDA, average winrate, average masteryLvl
    Y = [] #winner?
	
    for tu in data:
        matchId = tu[0]
        win1 = tu[9]

        #This is really slow, I dont have to search the whole csv
        participants = [p for p in participantInfo if p[0] == matchId]

        #Team 1
        kda1, winrate1, masteryLvl1 = getAverages(participants[0:5])
    
        #Team 2
		#kda2, winrate2, masteryLvl2 = getAverages(participants[5:10])
    
        X.append((kda1, winrate1, masteryLvl1))
        Y.append(win1)
			
    return X,Y

def getAverages(participants):
    kda, winrate, masteryLvl = 0, 0, 0
    for p in participants:
        kda += p[6]
        winrate += p[10]
        masteryLvl += p[12]
    
    l = len(p)

    return kda/float(l), winrate/float(l), masteryLvl/float(l)

def main():
    dataset = np.recfromcsv("matches.csv", delimiter=",")
    participantInfo = np.recfromcsv("participantInfo.csv", delimiter=",")
    
    XTrain, YTrain = formatData(dataset[0:700], participantInfo)
    
    clf = svm.SVC()
    clf.fit(XTrain, YTrain)
        
    XTest, YTest = formatData(dataset[700:900], participantInfo)
    
    YPredicted = []
    for x in XTest:
        YPredicted.append(clf.predict([list(x)]))
    
    print accuracy_score(YTest, YPredicted)

if __name__ == '__main__':
    main()