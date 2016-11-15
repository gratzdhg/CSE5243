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

def main(k, filenum = 2):
	#    path="/home/0/srini/WWW/674/public/reuters/"
	path = "./"
	filename1="out1.xml"
	filename2="out2.xml"
	filename=""
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
	m = m[range(0,int(m.shape[0]*.05)),:]
	numDocs = m.get_shape()[0]
	numWords = m.get_shape()[1]
	print "Docs: "+str(numDocs)
	sigs = []
	minhashTimes = [0] * len(k)
	error = [0] * len(k)
	for kVal in k:
		temp = time.time()
		hasher = minhash.MinHash(kVal)
		sigs.append(hasher.bucketData(m))
		temp -= time.time()
		print "Min Hash Construction for "+str(kVal)
		print "in "+str(-1*temp)
		minhashTimes.append(0.0)
	jaccardTime = 0.0
	numDocPairs = 0
	nonZero = []
	for i in range(0,numDocs):
		nonZero.append(sorted(sparse.find(m[i])[1]))
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
				error[l] += abs(minHashSim - sim)/sim
			numDocPairs += 1
	print "End Comparison"
	print "Jaccard Time: "+str(-1*jaccardTime)
	for i, kVal in enumerate(k):
		print "For "+str(kVal)
		print "Min Hash Time: "+str(-1*minhashTimes[i])
		print "Relative Mean Error: %"+str(error[i]*100/numDocPairs)
	
