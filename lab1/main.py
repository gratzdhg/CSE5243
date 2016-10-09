#!/usr/local/python-2.7.10/bin/python2.7
import scanner
from xmlhandler import XMLHandler
from xml.sax import make_parser
from sklearn.tree import DecisionTreeClassifier
from scipy import sparse
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer

def main():
	#    path="/home/0/srini/WWW/674/public/reuters/"
	path = "./"
	filename1="out1.xml"
	filename2="out2.xml"
	reader = make_parser()
	handler = XMLHandler()
	reader.setContentHandler(handler)
	datasource = open(filename1,"r")
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
	depth = 2
	tree = ""
	try:
		tree = pickle.load(open("treeout_depth"+str(depth)+".bin","r"))
	except IOError:
		tree = DecisionTreeClassifier(max_depth=2)
		tree.fit(buildData,buildTopics)
		pickle.dump(tree, open("treeout_depth2.bin","w"))
	print "************ Finished Tree Build *************"
	result = ""
	return tree.predict_proba(verifyData)
	resultPair = []
	for i, val in enumerate(result):
		val.sort()
		verifyTopics[i].sort()
		for j, topic in enumerate(val):
			resultPair = (topic, verifyTopics[i][j])
	return resultPair
	#    print str(reuters)
	#    reuters.printFileXML1(filename1)
	#    reuters.printFileXML2(filename2)
	
def main2(split = .7, filenum = 2):
		#    path="/home/0/srini/WWW/674/public/reuters/"
	path = "./"
	filename1="out1.xml"
	filename2="out2.xml"
	filename=""
	if filenum == 2:
		filename = filename2
	else:
		filename = filename1
	reader = make_parser()
	handler = XMLHandler()
	reader.setContentHandler(handler)
	datasource = open(filename,"r")
	reader.parse(datasource)
	m = handler.getMatrix().tocsr()
	
#	length = 0
#	for topic in handler.fullTopicList:
#		if length < len(topic):
#			length = len(topic)
#	for topic in handler.fullTopicList:
#		while len(topic) < length:
#			topic.append(-1)

	topics = []
	for topic in handler.fullTopicList:
		for t in topic:
			if t not in topics:
				topics += [t]
	
	# 70/30 split by default
	buildData = m[range(0,int(m.shape[0]*split)),:]
	verifyData = m[range(int(m.shape[0]*split),m.shape[0]),:]
	buildTopics = handler.fullTopicList[0:int(len(handler.fullTopicList)*split)]
	verifyTopics = handler.fullTopicList[int(len(handler.fullTopicList)*split):len(handler.fullTopicList)]
	
	neighbors = 1
	
	print "### done building things ###"

	mlb_build = MultiLabelBinarizer(classes=topics, sparse_output=False)
	new_b_topics = mlb_build.fit_transform(buildTopics)
	mlb_verify = MultiLabelBinarizer(classes=topics, sparse_output=False)
	new_v_topics = mlb_verify.fit_transform(verifyTopics)
		
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	neigh.fit(buildData,new_b_topics)
	
	predictions = neigh.predict(verifyData)
	total = 0
	score1 = 0
	similarity = predictions - new_v_topics
	for r in similarity:
		total += 1
		all_zero = True
		for c in r:
			if c != 0:
				all_zero = False
			if not all_zero:
				break
		if all_zero:
			score1 += 1
	print "exact / total = " + str(score1) + " / " + str(total) + " = " + str(score1/float(total))
	return [score1,total]
	
	
if __name__ == "__main__":
	main2()

