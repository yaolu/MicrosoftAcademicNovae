#!/usr/bin/python
import networkx as nx

def network_init(isdirected):
	if isdirected:
		G = nx.read_edgelist('result/bib.txt', nodetype=str, data=(('weight',float),),create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist('result/bib.txt', nodetype=str, data=(('weight',float),))

	node_val = {}

	with open('result/qua.txt') as fs:
		for line in fs:
			tmp = line.split()
			node_val.update({tmp[0]:float(tmp[1])})

	for key in G.nodes():
		try:
			G.node[key].update({'quality':node_val[key]})
		except KeyError, e:
			G.node[key].update({'quality':0.0})
	return G

