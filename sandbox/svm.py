#!/usr/bin/python

import sys
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score

def formatData(data, participantInfo):
    X = [] #average KDA, average winrate, average masteryLvl
    Y = [] #winner?

    counter = 0
    for tu in data:
        matchId = tu[0]
        win1 = tu[9]

        participants = []
        participants.append(participantInfo[(counter*10)])
        participants.append(participantInfo[(counter*10) + 1])
        participants.append(participantInfo[(counter*10) + 2])
        participants.append(participantInfo[(counter*10) + 3])
        participants.append(participantInfo[(counter*10) + 4])

        #Team 1
        kda1, winrate1, masteryLvl1 = getAverages(participants)
    
        X.append((kda1, winrate1, masteryLvl1))
        Y.append(win1)
        
        counter = counter + 1
			
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
    
    trainDataEnd = 700
    testDataEnd = 900
    
    XTrain, YTrain = formatData(dataset[0:trainDataEnd], participantInfo)
    
    clf = svm.SVC()
    clf.fit(XTrain, YTrain)
        
    XTest, YTest = formatData(dataset[trainDataEnd:testDataEnd], participantInfo[trainDataEnd*10:])
    
    YPredicted = []
    for x in XTest:
        YPredicted.append(clf.predict([list(x)]))
    
    print accuracy_score(YTest, YPredicted)

if __name__ == '__main__':
    main()