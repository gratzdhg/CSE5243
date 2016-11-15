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

def main(k, outfile, split = .3, numTrials = 10, startTrial = 0, filenum = 2):
	#    path="/home/0/srini/WWW/674/public/reuters/"
	path = "./"
	filename1="out1.xml"
	filename2="out2.xml"
	filename=""
	out = open(outfile,"w")
	if filenum == 2:
		filename = filename2
	else:
		filename = filename1
	print "Begin Data Read"
	reader = make_parser()
	handler = XMLHandler()
	reader.setContentHandler(handler)
	datasource = open(filename,"r")
	reader.parse(datasource)
	m = handler.getMatrix().tocsr()
	print "End Data Read"
	numDocs = m.shape[0]
	for i in range(startTrial, numTrials):
		minhashCompare(k, m[[d % numDocs for d in range((int(numDocs*split)*i),(int(numDocs*split)*(i+1)))],:], out)

def minhashCompare(k, m, out):
	numDocs = m.get_shape()[0]
	numWords = m.get_shape()[1]
	out.write("Docs: "+str(numDocs)+"\n")
	sigs = []
	minhashTimes = [0] * len(k)
	error = [0] * len(k)
	for kVal in k:
		temp = time.time()
		hasher = minhash.MinHash(kVal)
		sigs.append(hasher.bucketData(m))
		temp -= time.time()
		out.write("Min Hash Construction for "+str(kVal)+"\n")
		out.write("in "+str(-1*temp)+"\n")
		minhashTimes.append(0.0)
	jaccardTime = 0.0
	numDocPairs = 0
	nonZero = []
	for i in range(0,numDocs):
		nonZero.append(set(sparse.find(m[i])[1]))
	print "Begin Comparison"
	print "Document: "
	for i in range(0, numDocs):
		print str(i)
		for j in range(i+1, numDocs):
			tempTime = time.time()
			sim = simNonZ(nonZero[i], nonZero[j], numWords)
			jaccardTime += tempTime - time.time()
			for l in range(0,len(k)):
				tempTime = time.time()
				minHashSim = minhash.compare(sigs[l][i],sigs[l][j])
				minhashTimes[l] += tempTime - time.time()
				error[l] += (minHashSim - sim) ** 2
			numDocPairs += 1
	print "End Comparison"
	out.write("Jaccard Time: "+str(-1*jaccardTime)+"\n")
	for i, kVal in enumerate(k):
		out.write("For "+str(kVal)+"\n")
		out.write("Min Hash Time: "+str(-1*minhashTimes[i])+"\n")
		out.write("Mean Squared Error: %"+str(error[i]*100/numDocPairs)+"\n")
	
