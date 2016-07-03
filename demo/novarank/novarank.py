#!/usr/bin/python

from utils import network_init

class pagerank:
	def __init__(self,graph):
		self.graph =  graph
		self.d = 0.85
		self.V = len(self.graph)
		self.valuerank = {}

	def rank(self,isdirected):
		for key,node in self.graph.nodes(data = True):
			self.valuerank[key] = node.get('quality')

		if isdirected:
			print "directed version"
			
			
			for _ in range(10):
				print _
				for key in self.graph.nodes():
					rank_sum = 0
					neighbors = self.graph.neighbors(key)
					for nn in neighbors:
						nn_neigh = self.graph.neighbors(nn)
						all_influence = 0
						for nn_neigh_item in nn_neigh:
							#print nn, nn_neigh_item, self.valuerank[nn_neigh_item],self.graph.get_edge_data(nn,nn_neigh_item)['weight']
							all_influence += self.valuerank[nn_neigh_item]*self.graph.get_edge_data(nn,nn_neigh_item)['weight']
						all_influence += 0.0000001
						rank_sum += (self.graph.get_edge_data(key,nn)['weight']*self.valuerank[nn]*self.valuerank[key])/all_influence
					self.valuerank[key] = ((1 - float(self.d)) * (1/float(self.V))) + self.d*rank_sum


G = network_init(isdirected=True)
p = pagerank(G)
p.rank(isdirected=True)
print p.valuerank