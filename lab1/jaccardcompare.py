import itertools
from scipy import sparse

def similarity(data1, data2):
	length = data1.get_shape()[1]
	nonZero1 = sparse.find(data1)[1]
	nonZero2 = sparse.find(data2)[1]
	return simNonZ(nonZero1, nonZero2, length)

def simNonZ(nonZero1, nonZero2, length):
	intersect = len(nonZero1.union(nonZero2))
	if intersect == 0:
		return 0
	return float(len(nonZero1.intersection(nonZero2)))/intersect

