#!/usr/bin/python

import sys
import numpy as np
from sklearn import tree

import RankMapping;

def main():
    dataset = np.recfromcsv("test.csv", delimiter=",")
    
    X = []
    Y = []

    for tu in dataset:
        X.append((tu[10], tu[11], tu[12], RankMapping.map[tu[8]])); #Kills, Deaths, Assists, Highest Rank
        Y.append((tu[9])) #Winner  (True or False)
    
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)

    print clf.predict([[15,6,10, RankMapping.map['GOLD']]])
    print clf.predict([[5,15,10, RankMapping.map['DIAMOND']]])
    print clf.predict([[0,5,15, RankMapping.map['BRONZE']]])
    print clf.predict([[0,5,15, RankMapping.map['DIAMOND']]])

if __name__ == '__main__':
    main()