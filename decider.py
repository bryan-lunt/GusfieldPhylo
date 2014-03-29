#!/usr/bin/env python

import sys

sys.setrecursionlimit(500000)

import scipy as S
FILE = sys.argv[-1]

def readfile(filename):
	retarr = []
	file = open(filename)
	for line in file:
		retarr.append([int(i) for i in line.strip()])
	file.close()
	return retarr

def asbin(myarr):
	retval = 0
	for bit in myarr:
		retval = retval << 1
		retval += bit
	return retval

def radixSort(arraylike):
	sortArray = [(i, asbin(arraylike[i])) for i in range(len(arraylike))]


	digit = 1
	maxDigit = 2**len(arraylike)
	while digit <= maxDigit:
		firstlist = list()
		lastlist = list()

		for element in sortArray:
			if element[1] & digit:
				firstlist.append(element)
			else:
				lastlist.append(element)
		sortArray = firstlist + lastlist
		digit = digit << 1

	tmpstorage = S.zeros(arraylike.shape)
	assert len(sortArray) == arraylike.shape[0]
	for i in range(len(sortArray)):
		tmpstorage[i] = arraylike[sortArray[i][0]]

	arraylike[:,:] = tmpstorage

#for testing only!
def fakeSort(arraylike):
	sortArray = [(i, asbin(arraylike[i])) for i in range(len(arraylike))]
	sortArray.sort(key=lambda x: x[1],reverse=True)

	tmpstorage = S.zeros(arraylike.shape)
	assert len(sortArray) == arraylike.shape[0]
	for i in range(len(sortArray)):
		tmpstorage[i] = arraylike[sortArray[i][0]]

	arraylike[:,:] = tmpstorage


trackset = set()

def split(anArray,digit,width):
	if len(anArray) == 0 or digit >= width:
		return anArray
	left = []
	right = []
	for i in anArray:
		if i[digit] == 0:
			left.append(i)
		else:# i[digit] == 1:
			right.append(i)
		#else:
		#	raise Exception("can't bifurcate")

	if len(left) == 0:
		return split(right,digit+1,width)
	elif len(right) == 0:
		return split(left,digit+1,width)
	else:
		if digit in trackset:
			raise Exception("NOOOOO!")
		else:
			trackset.add(digit)
		split(left,digit+1,width)
		split(right,digit+1,width)
		#return (digit, split(left,digit+1),split(right,digit+1))



import time

print "BEGIN"
time1 = time.time()

a = S.array(readfile(FILE))

radixSort(a.T)
print "Done Sorting", time.time() - time1
try:
	roottree = split(a,0,a.shape[1])
except Exception as e:
	print "FAILURE", e
else:
	"SUCCESS"

time2 = time.time()
total = time2 - time1

aShape = a.shape
print a.shape[0]*a.shape[1], total
