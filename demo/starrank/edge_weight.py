#!/usr/bin/python2.7
import numpy as np
from collections import Counter
from itertools import combinations

class count_user_info:
	
	def __init__(self,datafile):
		self._all_pubs = []
		self._all_coauthors = []
		with open(datafile) as fs:
				for line in fs:
					self._all_pubs.append(line.strip('\n').split())

	def user_publication_count(self):
		return Counter(np.concatenate(self._all_pubs))

	def user_co_author_count(self):
		for item in self._all_pubs:
			self._all_coauthors+=list(combinations(item, 2))
		return Counter(self._all_coauthors)




def bibliography_generate(infile,outfile):

#infile should like data/AuId_AuId.txt
	bibliography_network = count_user_info(infile)
#a.read_datafile()
	pub_count = bibliography_network.user_publication_count()
	coauthor_count = bibliography_network.user_co_author_count()
#print list(coauthor)[0:3]
#print pub_count['1553700638']
	stat = []
	with open(outfile,'a+') as fs:
		for i in coauthor_count:
			nn = coauthor_count[i]
			try:
				zz = coauthor_count[(i[1],i[0])]
			except KeyError, e:
				zz = 0
			#fs.write(i[0]+'\t'+i[1]+'\t'+str(nn)+'\t'+str(zz)+'\t'+str(nn+zz)+'\t'+str(pub_count[i[1]])+'\n')
			fs.write(i[0]+'\t'+i[1]+'\t'+str(nn+zz)+'\t'+str(pub_count[i[1]])+'\n')
	

bibliography_generate('data/AuId_AuId.txt', '/tmp/test.txt')

