#!/usr/local/python-2.7.10/bin/python2.7
import apply_rules
import time

def main(rulesdoc = "./rout4_4_5.txt", maxNumTopics = 5):
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
	docFile.close()
	print "End Data Read"
	print "Read in Rules"
	t2 = time.time()
	rules = apply_rules.sort_rules(rulesdoc)
	t2 = time.time() - t2
	print "Apply Rules"
	t = time.time()
	result = apply_rules.apply_rules(docs,rules,maxNumTopics);
	t = time.time() - t
	print "Compute Accuracy"
	countCorrect = 0
	count = 0
	countCorrectAll = 0
	countAll = 0
	for i in range(0,min(len(result),len(topics))):
		lenResult = len(result[i])
		lenTopic = len(topics[i])
		if lenTopic != 0:
			countCorrect += len(result[i] & topics[i])
			count += lenResult
		if lenTopic == 0 and lenResult == 0:
			countCorrectAll += 1
			countAll += 1
		else:
			countCorrectAll += len(result[i] & topics[i])
			countAll += max(lenTopic, lenResult)
	r = [count, countCorrect]
	rAll = [countAll, countCorrectAll]
 	print "[total, correct] = "+str(r)+" accuracy = "+ str(float(r[1])/r[0])
# 	print "Complete Count [total, correct] = "+str(rAll)+" accuracy = "+ str(float(rAll[1])/rAll[0])
	print "Rule Parsing Time "+str(t2)
	print "Classification Time "+str(t)

main("rout10_10.txt")
