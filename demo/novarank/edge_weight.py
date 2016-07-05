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

	pub_count = bibliography_network.user_publication_count()

	coauthor_count = bibliography_network.user_co_author_count()

	with open(outfile,'a+') as fs:
		for author_pair in coauthor_count:
			a_to_b = coauthor_count[author_pair]

			try:
				b_to_a = coauthor_count[(author_pair[1],author_pair[0])]

			except KeyError, e:
				b_to_a = 0
			#fs.write(i[0]+'\t'+i[1]+'\t'+str(nn)+'\t'+str(zz)+'\t'+str(nn+zz)+'\t'+str(pub_count[i[1]])+'\n')
			#fs.write(author_pair[0] + '\t' + author_pair[1] + '\t'+ str(a_to_b + b_to_a)+ '\t' + str(pub_count[author_pair[1]]) + '\n')
			fs.write(author_pair[0] + '\t' + author_pair[1] + '\t'+ str(float(a_to_b + b_to_a)/pub_count[author_pair[1]]) + '\n')


if __name__ == '__main__':
	bibliography_generate('data/2000/AuId_work_togethor_2000', 'result/bib_2000.txt')

