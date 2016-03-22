#!/usr/bin/python

import sys
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn import cross_validation

def formatData(data, participantInfo):
    X = [] #average KDA, average winrate, average masteryLvl
    Y = [] #winner?

    counter = 0
    for tu in data:
        matchId = tu[0]
        win1 = tu[9]
        win2 = tu[9+(8*16)]

        participants = []
        participants.append(participantInfo[(counter*10)])
        participants.append(participantInfo[(counter*10) + 1])
        participants.append(participantInfo[(counter*10) + 2])
        participants.append(participantInfo[(counter*10) + 3])
        participants.append(participantInfo[(counter*10) + 4])

        participants.append(participantInfo[(counter*10) + 5])
        participants.append(participantInfo[(counter*10) + 6])
        participants.append(participantInfo[(counter*10) + 7])
        participants.append(participantInfo[(counter*10) + 8])
        participants.append(participantInfo[(counter*10) + 9])

        #Team 1
        kda1, winrate1, masteryLvl1 = getAverages(participants[0:5])

        #Team 2
        kda2, winrate2, masteryLvl2 = getAverages(participants[5:10])
    
        #X.append((kda1, winrate1, masteryLvl1))
        #X.append((kda2, winrate2, masteryLvl2))
        #Y.append(win1)
        #Y.append(win2)
        X.append((kda1-kda2, winrate1-winrate2, masteryLvl1-masteryLvl2))
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
    
    #trainDataEnd = 700
    #testDataEnd = 900
    
    X, Y = formatData(dataset, participantInfo)
    """
    clf = svm.SVC()
    clf.fit(XTrain, YTrain)
        
    XTest, YTest = formatData(dataset[trainDataEnd:testDataEnd], participantInfo[trainDataEnd*10:])
    
    YPredicted = []
    for x in XTest:
        YPredicted.append(clf.predict([list(x)]))
    
    print accuracy_score(YTest, YPredicted)
"""
    svc = svm.SVC(kernel='linear', C=1)
    scores = cross_validation.cross_val_score(svc, X, Y, cv=10)
    print scores.mean()
    """
    X_folds = np.array_split(X, 10)
    y_folds = np.array_split(Y, 10)
    scores = list()
    for k in range(10):
        # We use 'list' to copy, in order to 'pop' later on
        X_train = list(X_folds)
        X_test  = X_train.pop(k)
        X_train = np.concatenate(X_train)
        y_train = list(y_folds)
        y_test  = y_train.pop(k)
        y_train = np.concatenate(y_train)
        scores.append(svc.fit(X_train, y_train).score(X_test, y_test))
    print(scores)"""

if __name__ == '__main__':
    main()