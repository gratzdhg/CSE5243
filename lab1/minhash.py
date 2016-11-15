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
			self.p =	982451653 
		self.buckets = {}
		self.aList = []
		self.bList = []
		self.N = 0
		for i in range(0,numPerms):
			self.aList.append(random.randint(10000000,1000000000000))
			self.bList.append(random.randint(10000000,1000000000000))

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
			for word in nonZero:
				if len(first) == 0:
					first = perm[word]
					continue
				for j in range(0,len(perm[word])):
					if first[j] > perm[word][j]:
						first[j] = perm[word][j]
			self.buckets[i] = first
		return self.buckets
