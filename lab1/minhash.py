import random
import itertools
from scipy import sparse

def compare(data1, data2):
	same = 0
	for i in range(0,len(data2)):
		if data1[i] == data2[i]:
			same += 1
	diff = len(data1) - same
	return float(same)/(same + 2*diff)
			

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
			self.aList.append(random.randint(0,1000000000000))
			self.bList.append(random.randint(0,1000000000000))

	def hashF(self,a,b,x):
		return ((a*x+b)%self.p)%self.N

	def bucketData(self, data):
		self.N = data.get_shape()[1]
		perm = {}
		for a, b in itertools.izip(self.aList,self.bList):
			for x in range(0,self.N):
					if x not in perm:
						perm[x] = []
					perm[x] += [self.hashF(a,b,x)]
		for i, row in enumerate(data):
#			print "row "+str(i)
			nonZero = sparse.find(row)[1]
			first = []
			for col in nonZero:
				for j, elem in enumerate(perm[col]):
					if j == len(first):
						first.append(elem)
					elif elem < first[j]:
						first[j] = elem 
			self.buckets[i] = first
		return self.buckets
