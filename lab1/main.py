#!/usr/local/python-2.7.10/bin/python2.7
import scanner
from xmlhandler import XMLHandler
from xml.sax import make_parser
from sklearn.tree import DecisionTreeClassifier
from scipy import sparse
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer

def main(split = .7, filenum = 2, depth = 16):
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
	length = 0
	for topic in handler.fullTopicList:
		if length < len(topic):
			length = len(topic)
	for topic in handler.fullTopicList:
		while len(topic) < length:
			topic.append(-1)
	print "************ Finished Import **************"
	buildData = m[range(0,int(m.shape[0]*split)),:]
	verifyData = m[range(int(m.shape[0]*split),m.shape[0]),:]
	buildTopics = handler.fullTopicList[0:int(len(handler.fullTopicList)*split)]
	verifyTopics = handler.fullTopicList[int(len(handler.fullTopicList)*split):len(handler.fullTopicList)]
	tree = ""
	treeFileName = "treeout_depth"+str(depth)+"_split"+str(int(split*100))+"_data"+str(filenum)+".bin"
	try:
		tree = pickle.load(open(treeFileName,"r"))
	except IOError:
		tree = DecisionTreeClassifier(max_depth=depth)
		tree.fit(buildData,buildTopics)
		pickle.dump(tree, open(treeFileName,"w"))
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
	
r = main(.7,1,2)
print "[total, correct] = "+str(r)+" accuracy = "+ str(float(r[1])/r[0])

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

