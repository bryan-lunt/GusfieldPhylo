import networkx as _nx

class SuffixTree(object):
	ROOT_NAME = "ROOT"
	def __init__(self):
		self.G = _nx.DiGraph()
		self.G.add_node(SuffixTree.ROOT_NAME)
	
	def add_leaf(self, path_list, name, enforce_tree=False):
		
		local_path_list = list()
		local_path_list.extend(path_list)
		#traverse the tree from the root until we run out of elements in path_list or in the tree.
		node_cursor=SuffixTree.ROOT_NAME
		while len(local_path_list) > 0:
			current_in_path = local_path_list.pop(0)
			if not self.G.has_edge(node_cursor, current_in_path):
				if enforce_tree and self.G.has_node(current_in_path):
					raise Exception("Not a perfect phylogeny")
				self.G.add_edge(node_cursor, current_in_path)
			node_cursor = current_in_path#traverse that edge
		self.G.add_edge(node_cursor,"L:" + str(name))
	
	def is_tree(self):
		isDAG = _nx.is_directed_acyclic_graph(self.G)
		degree = all([i[1] <= 1 for i in self.G.in_degree_iter()])

		return isDAG and degree

	def get_levels(self):
		level_list = list()
		next_level = set([SuffixTree.ROOT_NAME])
		while len(next_level) > 0:
			level_list.append(list(next_level))
			next_level = set()
			for a in level_list[-1]:
				for i in self.G.successors(a):
					next_level.add(i)
		return level_list

	def to_bio_tree(self):
		import Bio.Phylo.BaseTree as BT
		successor_dict = _nx.bfs_successors(self.G, SuffixTree.ROOT_NAME)
		
		T = BT.Tree(name=SuffixTree.ROOT_NAME)
		clade_dict = {SuffixTree.ROOT_NAME:T.clade}
	
		next_up = [ SuffixTree.ROOT_NAME]
		while len(next_up) > 0:
			current = next_up.pop(0)
			children = successor_dict.get(current,[])
			for c in children:
				new_clade = BT.Clade(name=c)
				clade_dict[c] = new_clade
				clade_dict[current].clades.append(new_clade)
			next_up.extend(children)

		return T



if __name__ == "__main__":
	import matplotlib.pyplot as plt
	A = SuffixTree()
	A.add_leaf(['c2', 'c1'], 's1')
	A.add_leaf(['c3'], 's2')
	A.add_leaf(['c2', 'c1', 'c5'], 's3')
	A.add_leaf(['c3', 'c4'], 's4')
	A.add_leaf(['c2'], 's5')
	_nx.draw(A.G)
	plt.show()
