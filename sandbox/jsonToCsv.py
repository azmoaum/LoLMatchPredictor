#!/usr/bin/python

""" An incomplete script which can be used to convert a json to csv by manually inputting column headers """
import csv
import json

filename = 'matches1.json'

def main():
    with open(filename) as data_file:
        data = json.load(data_file)
    
    f = csv.writer(open("test.csv", "wb+"))

    #Optional: write headers
    f.writerow(["matchId", "matchDuration"])

    for row in data['matches']:
        f.writerow([row['matchId'], row['matchDuration']])

if __name__ == '__main__':
    main()