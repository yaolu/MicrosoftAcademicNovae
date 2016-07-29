#!/usr/bin/python

import os
import numpy as np

#global first_or_not
#global machine_year

#first_or_not = True
#machine_year = 2016

def get_author_list(first_or_not):
	if first_or_not:
		authorlist = os.listdir('author_paper/first/')
	else:
		authorlist = os.listdir('author_paper/non-first/')

	return authorlist

def get_author_publist(authorid,count_year,first_or_not):
	if first_or_not:
		author_pub_filepath = 'author_paper/first/'+authorid
		publist = np.loadtxt(author_pub_filepath,dtype=str)
	else:
		author_pub_filepath = 'author_paper/non-first/'+authorid
		publist = np.loadtxt(author_pub_filepath,dtype=str,delimiter='\t')
	#print publist
	if len(publist[0])!= 2:
		return [publist[0]]
	else:
		return [pub[0] for pub in publist if int(pub[1]) <= count_year]

def get_paper_cite(paperid, count_year):
	count = 0
	if os.path.isfile('inacl_cite/'+paperid):
		with open('inacl_cite/'+paperid) as fs:
			for line in fs:
				if int(line.split()[1]) <= count_year:
					count += 1
	
	return count
	

def main(machine_year):
	authorlist = get_author_list(first_or_not = True)

	for author in authorlist:
		#print author
		author_all_publist = get_author_publist(authorid = author, first_or_not = True, count_year = machine_year)
		paper_cite_count = 0
		for paperid in author_all_publist:
			paper_cite_count += get_paper_cite(paperid, machine_year)
		#print author,paper_cite_count
		with open('/tmp/author_cite_count_'+ str(machine_year)+'.txt','a+') as fs:
			fs.write(author+'\t'+str(paper_cite_count)+'\n')

if __name__ == '__main__':
	main(machine_year=2010)