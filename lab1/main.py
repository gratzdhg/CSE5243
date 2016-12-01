#!/usr/local/python-2.7.10/bin/python2.7
import scanner
from xmlhandler import XMLHandler
from xml.sax import make_parser
from sklearn.tree import DecisionTreeClassifier
from scipy import sparse
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import time
import minhash
from jaccardcompare import simNonZ

def main():
	filename = "./testing.txt"
	docs = []
	topics = []
	print "Begin Data Read"
	docFile = open(filename,'r')
	for line in docFile:
		wordset = set()
		topicset = set()
		for word in line.split(" "):
			if not word.startswith(":"):
				wordset.add(word)
			else:
				topicset.add(word)
		docs.append(wordset)
		topics.append(topicset)
	print "End Data Read"
	return topics

main()
