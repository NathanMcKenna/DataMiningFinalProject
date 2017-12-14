# -*- coding: utf-8 -*-

#William Cooper
#Data Mining
#CU Boulder
#Information code adapted from https://gist.github.com/iamaziz/02491e36490eb05a30f8 by Aziz Alto

from __future__ import division
from math import log

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

#Normalizes data between 0 and 1
def normalize(list):
    return [float(i)/max(list) for i in list]

#Removes spaces from list
def removespaces(list):
    return [i for i in list if i != '']

#Places new, normalized data into the spots where the old data used to be
def replacedata(newdata, olddata):
    index = 0
    for i in range (1, len(olddata)):
        if olddata[i] != '':
            olddata[i] = newdata[index]
            index = index + 1

#Removes dollar signs for a column that contains monetary values
def removedollasigns(list):
    list = [x.replace("$", "") for x in list]
    list = [x.replace(",", "") for x in list]
    return list

#Normalizes data, then replaces old data with normalized data
def normalizealldata(ogdata):
    for i in range (0, len(ogdata)):
        if i == 17:
            ogdata[i] = removedollasigns(ogdata[i])
        if i != 0 and i != 1 and i != 2 and i != 13 and i != 14 and i != 33:
            #print ogdata[i]
            newdata = [x for x in ogdata[i]]
            newdata.pop(0)
            newdata = removespaces(newdata)
            newdata = [float(x) for x in newdata]
            newdata = normalize(newdata)
            replacedata(newdata, ogdata[i])

#Goes through nomrmalized data and assigns it a category based on the scale 0-0.2=1 0.2-0.4=2 0.4-0.6=3 etc. up to 5
def categorizedata(data):
    for i in range(1, len(data)):
        if i != 0 and i != 1 and i != 2 and i != 13 and i != 14 and i != 33:
            for j in range(0, len(data[i])):
                if data[i][j] < 0.2:
                    data[i][j] = 1
                elif data[i][j] >= 0.2 and data[i][j] < 0.4:
                    data[i][j] = 2
                elif data[i][j] >= 0.4 and data[i][j] < 0.6:
                    data[i][j] = 3
                elif data[i][j] >= 0.6 and data[i][j] < 0.8:
                    data[i][j] = 4
                elif data[i][j] >= 0.8 and data[i][j] <= 1:
                    data[i][j] = 5

#Changes the happiness ranking to either "happy" if the country is in the top 50% of happiness, or
#"unhappy" if the country is in the bottom 50%. Then, goes through each category and calculates total number of
#happy and unhappy countries and outputs this list
def classifyhappiness(data):
    happtots = []
    length = 0
    for i in range(1, len(data[2])):
        if data[2][i] != '':
            data[2][i] = int(data[2][i])
            if data[2][i] > 79:
                data[2][i] = "happy"
            else:
                data[2][i] = "unhappy"
    for i in range(1, len(data)):
        unhappcount = 0
        happcount = 0
        if i != 0 and i != 2 and i != 3 and i != 4 and i!= 5 and i != 13 and i != 33:
            for j in range (0, len(data[i])):
                if data[i][j] != '':
                    if data[2][j] == "happy":
                        happcount += 1
                    elif data[2][j] == "unhappy":
                        unhappcount += 1
            happtots.append([happcount, unhappcount])

    return happtots

#Goes through each relevant attribute and for each class within an attribute, calculates the number of
# happy and unhappy countries
def classifyattributes(data):
    allcats = []
    allcounts = []
    allsepcounts = []
    labels = []
    for i in range(1, len(data)):
        if i != 0 and i != 2 and i != 3 and i != 4 and i != 5 and i != 13 and i != 33:
            cats = []
            counts = []
            sepcounts = []
            labels.append(data[i][0])
            for j in range (1, 158):
                if data[i][j] != "":
                    if data[i][j] in cats:
                        index = cats.index(data[i][j])
                        counts[index] += 1
                        if data[2][j] == "unhappy":
                            sepcounts[index][1] += 1
                        elif data[2][j] == "happy":
                            sepcounts[index][0] += 1
                    else:
                        cats.append(data[i][j])
                        counts.append(1)
                        sepcounts.append([0, 0])
                        if data[2][j] == "unhappy":
                            sepcounts[len(sepcounts) - 1][1] += 1
                        elif data[2][j] == "happy":
                            sepcounts[len(sepcounts) - 1][0] += 1

            allcats.append(cats)
            allcounts.append(counts)
            allsepcounts.append(sepcounts)

    return allcats, allcounts, allsepcounts, labels


#Reads in CSV from the 'finalmerge.csv' file
data = []
numindices = []


with open('finalmerge.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data.append(row)

#Transposesdata to work with columns
coldata = map(list, zip(*data))

#Normalize
normalizealldata(coldata)

#Categorize
categorizedata(coldata)

#Get happiness totals
happy =  classifyhappiness(coldata)

#Get classification within attribute totals
cats, counts, sepcounts, labels =classifyattributes(coldata)


#Adapted from the repository listed above, calculates information gain using the entropy method
def entropy(pi):
    '''
    return the Entropy of a probability distribution:
    entropy(p) = − SUM (Pi * log(Pi) )
    defintion:
            entropy is a metric to measure the uncertainty of a probability distribution.
    entropy ranges between 0 to 1
    Low entropy means the distribution varies (peaks and valleys).
    High entropy means the distribution is uniform.
    See:
            http://www.cs.csi.cuny.edu/~imberman/ai/Entropy%20and%20Information%20Gain.htm
    '''

    total = 0
    for p in pi:
        p = p / sum(pi)
        if p != 0:
            total += p * log(p, 2)
        else:
            total += 0
    total *= -1
    return total


def gain(d, a):

    total = 0
    for v in a:
        total += sum(v) / sum(d) * entropy(v)

    gain = entropy(d) - total
    return gain

#Calculate information gain for each relevant attribute in data set with respect to happiness
gainz =[]
for i in range(0, len(sepcounts)):
    if i != 0 and i != 2 and i != 3 and i != 4 and i != 5 and i != 13 and i != 33:
        gainz.append([gain(happy[i], sepcounts[i]), labels[i]])
        print "Category:", labels[i]
        print "Information Gain:", gain(happy[i], sepcounts[i])
        print

sortedgainz =  sorted(gainz)
sortedgainz.reverse()

#Prints information gain and attribute in decreasing order
print sortedgainz