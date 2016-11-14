import itertools
from scipy import sparse

def similarity(data1, data2):
	length = data1.get_shape()[1]
	nonZero1 = sparse.find(data1)[1]
	nonZero2 = sparse.find(data2)[1]
	simNonZ(nonZero1, nonZero2, length)

def simNonZ(nonZero1, nonZero2, length):
	same = 0
	diff = 0
	i = 0
	j = 0
	minLen = min(len(nonZero1), len(nonZero2))
	while max(i,j) < minLen:
		if nonZero1[i] == nonZero2[j]:
			same += 1
			i += 1
			j += 1
		elif nonZero1[i] > nonZero2[j]:
			diff += 1
			j += 1
		elif nonZero1[i] < nonZero2[j]:
			diff += 1
			i += 1 
	diff += max(len(nonZero1) - i,len(nonZero2) - j)
	bothZero = length - same - diff
	intersect = bothZero + same
	union = bothZero + same + 2*diff
	return float(intersect)/union
