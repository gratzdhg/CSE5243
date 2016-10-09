#!/usr/local/python-2.7.10/bin/python2.7
import scanner
from xmlhandler import XMLHandler
from xml.sax import make_parser
from sklearn.tree import DecisionTreeClassifier
from scipy import sparse
import pickle

def main():
	#    path="/home/0/srini/WWW/674/public/reuters/"
	path = "./"
	filename1="out1.xml"
	filename2="out2.xml"
	reader = make_parser()
	handler = XMLHandler()
	reader.setContentHandler(handler)
	datasource = open(filename2,"r")
	reader.parse(datasource)
	m = handler.getMatrix().tocsr()
	length = 0
	for topic in handler.fullTopicList:
		if length < len(topic):
			length = len(topic)
	for topic in handler.fullTopicList:
		while len(topic) < length:
			topic.append(-1)
	print "************ Finished Import **************"
	split = .7 #70/30 split
	buildData = m[range(0,int(m.shape[0]*split)),:]
	verifyData = m[range(int(m.shape[0]*split),m.shape[0]),:]
	buildTopics = handler.fullTopicList[0:int(len(handler.fullTopicList)*split)]
	verifyTopics = handler.fullTopicList[int(len(handler.fullTopicList)*split):len(handler.fullTopicList)]
	depth = 64
	tree = ""
	try:
		tree = pickle.load(open("treeout_depth"+str(depth)+"_goodData.bin","r"))
	except IOError:
		tree = DecisionTreeClassifier(max_depth=depth)
		tree.fit(buildData,buildTopics)
		pickle.dump(tree, open("treeout_depth"+str(depth)+"_goodData.bin","w"))
	print "************ Finished Tree Build *************"
	result = tree.predict(verifyData)
	countCorrect = 0
	count = 0
	for i, val in enumerate(result):
		val.sort()
		verifyTopics[i].sort()
		resultPair = []
		allNone = True
		for j, topic in enumerate(val):
			if verifyTopics[i][j] != -1:
				allNone = False
				count += 1
				if topic == verifyTopics[i][j]:
					countCorrect += 1
			elif topic != -1:
				count += 1
				allNone = False
		if allNone:
			count += 1
			countCorrect += 1
				
	return [count, countCorrect]
	#    print str(reuters)
	#    reuters.printFileXML1(filename1)
	#    reuters.printFileXML2(filename2)
	
r = main()
print r
print float(r[1])/r[0]
