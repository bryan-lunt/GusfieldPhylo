#!/usr/bin/env python

import scipy as S
import networkx as nx

import matplotlib.pyplot as plt
from SuffixTree import *

#temporary crap
def readfile(filename):
	retarr = []
	file = open(filename)
	for line in file:
		retarr.append([int(i) for i in line.strip()])
	file.close()
	return S.array(retarr,S.int_) 

def to_binary(in_list):
	retval = 0
	for bit in in_list:
		retval = (retval << 1) + bit
	return retval

def from_binary_to_prefix(in_bin, names):
	prefix_list = list()
	local_names = list()
	local_names.extend(names)
	while in_bin > 0:
		cur_symbol = local_names.pop()
		if in_bin & 1:
			prefix_list.append(cur_symbol)
		in_bin = in_bin >> 1
	prefix_list.reverse()
	return prefix_list

def pattern_equivelent(a,b):
	return all(a == b) or all((1-a) == b)

#remove equivelent patterns
def consolidate_patterns(snv_matrix):
	patterns = snv_matrix.T

	def equivelent(a,b):
		return all(a == b) or all((1-a) == b)

	#yeah, it's O(n^2)...
	out_patterns = list()
	out_pattern_ids = list()
	
	for one_pat_index in range(len(patterns)):
		new_pattern = True
		for exist_pat_index in range(len(out_patterns)):
			if equivelent(patterns[one_pat_index], out_patterns[exist_pat_index]):
				out_pattern_ids[exist_pat_index].append(one_pat_index)
				new_pattern = False
				break
		
		if new_pattern:
			out_patterns.append(patterns[one_pat_index])
			out_pattern_ids.append([one_pat_index])
	
	out_pattern_ids = [';'.join(map(lambda x:str(x), i)) for i in out_pattern_ids]

	return S.array(out_patterns,S.int_).T, S.array(out_pattern_ids)


def gussman_algorithm(SNVs):
	
	reduced_align, patids = consolidate_patterns(SNVs)
	#sort: Gussfield calls for radix, we just use our own.
	pats_bin = S.array(map(to_binary, reduced_align.T), S.int_)
	
	ordering = pats_bin.argsort()
	
	reduced_align = reduced_align[:,ordering[::-1]]

	reduced_bin = S.array(map(to_binary, reduced_align), S.int_)

	as_prefixes = [from_binary_to_prefix(row, patids) for row in reduced_bin]
	with_names = zip(as_prefixes, ['S' + str(i) for i in range(len(as_prefixes))])

	SuffTree = SuffixTree()

	for path, name in with_names:
		try:
			SuffTree.add_leaf(path, name)
		except:
			print "difficulty adding : " + repr(path) + " : " + name

	

	return SuffTree

	


if __name__ == "__main__":
	import sys
	test = readfile(sys.argv[-1])
	test = S.array(S.hstack([S.ones(test.shape[0]).reshape(-1,1), test]),S.int_)


	myTree = gussman_algorithm(test)
	
	if not myTree.is_tree():
		print "COULD NOT CREATE A VALID TREE"
	
	nx.draw_networkx(myTree.G, pos=nx.shell_layout(myTree.G, myTree.get_levels()))
	plt.show()
