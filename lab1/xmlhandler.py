import os
from numpy import array
from scipy.sparse import coo_matrix
from xml.sax.handler import ContentHandler

class XMLHandler(ContentHandler):
	def __init__(self):
		self.fullTopicList = []
		self.fullPlaceList = []
		self.data = []
		self.rowIndex = []
		self.colIndex = []
		self.wordPosMap = {}
		self.wordPosInc = int(0)
		self.numDocs = int(0)
	def startElement(self, name, attrs):
		if name == "document":
			self.topicList = []
			self.placeList =[]
	def endElement(self, name):
		if name == "document":
			self.numDocs += 1
			self.fullTopicList.append(self.topicList)
			self.topicList = []
			self.fullPlaceList.append(self.placeList)
			self.placeList = []
		elif name == "place":
			self.checkWord(self.value)
			self.placeList.append(self.wordPosMap[self.value])
		elif name == "topic":
			self.checkWord(self.value)
			self.topicList.append(self.wordPosMap[self.value])
		elif name == "feature":
			split = self.value.split(" : ",2)
			if len(split) < 2:
#				print str(split) + " " + str(self.value)
				return
			self.checkWord(split[0])
			self.data.append(float(split[1]))
			self.colIndex.append(self.numDocs)
			self.rowIndex.append(self.wordPosMap[split[0]])
	def characters(self,content):
		self.value = content
	def getMatrix(self):
		return coo_matrix((self.data,(self.colIndex, self.rowIndex)), shape=(max(self.colIndex)+1,max(self.rowIndex)+1))
	def checkWord(self, word):
		if word not in self.wordPosMap:
			self.wordPosMap[word] = self.wordPosInc
			self.wordPosInc += 1

