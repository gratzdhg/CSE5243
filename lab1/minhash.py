import random
import itertools
from scipy import sparse

def compare(data1, data2):
	same = 0
	for i in range(0,len(data2)):
		if data1[i] == data2[i]:
			same += 1
	return float(same)/len(data2)
			

class MinHash:
	def __init__(self, numPerms, p = None):
		if p is not None:
			self.p = p
		else:
			self.p = 15485863	#982451653 
		self.buckets = []
		self.aList = []
		self.bList = []
		self.N = 0
		for i in range(0,numPerms):
			newA = random.randint(7,15485863)
			while newA in self.aList:
				newA = random.randint(7,15485863)
			self.aList.append(newA)
			newB = random.randint(17,982451653)
			while newB in self.bList:
				newB = random.randint(17,982451653)
			self.bList.append(newB)

	def hashF(self,a,b,x):
		return ((a*x+b)%self.p)%self.N

	def bucketData(self, data):
		self.N = data.get_shape()[1]
		perm = []
		for x in range(0,self.N):
			perm.append([])
			for i in range(0,len(self.aList)):
					perm[x].append(self.hashF(self.aList[i],self.bList[i],x))
		for i, doc in enumerate(data):
			nonZero = sparse.find(doc)[1]
			first = []
			words = []
			for word in nonZero:
				if len(first) == 0:
					first = [self.N+1] * len(perm[word])
					words = [word] * len(perm[word])
				for j in range(0,len(perm[word])):
					if first[j] > perm[word][j]:
						first[j] = perm[word][j]
						words[j] = word
			self.buckets.append(first)
		return self.buckets
