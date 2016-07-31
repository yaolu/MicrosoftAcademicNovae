#!/usr/bin/python
from collections import Counter
import os



def cooperation_count():
	coo_data = []
	with open('/tmp/cooperation.csv') as fs:
		for line in fs:
			coo_data.append(line.strip('\n'))

	coo_dict = Counter(coo_data)
	#print coo_dict
	rev_coo_dict ={}
	for key in coo_dict:
		key_split = key.strip('\n').split('\t')
		#print key_split
		try:
			reverse_coo = coo_dict[key_split[1]+'\t'+key_split[0]]
		except KeyError as e:
		#	print 'no reverse'
			reverse_coo = 0
		rev_coo_dict.update({key_split[0]+'\t'+key_split[1]:reverse_coo+coo_dict[key]})
		rev_coo_dict.update({key_split[1]+'\t'+key_split[0]:reverse_coo+coo_dict[key]})
	return coo_data, rev_coo_dict

def pub_count():
	pub_data = {}
	with open('/tmp/quality.csv') as fs:
		for line in fs:
			pub_data.update({line.split('\t')[0]:int(line.split('\t')[1])})
	return pub_data


def cite_count():
	cc_data = {}
	with open('/tmp/author_cite_count_2005.txt') as fs:
		for line in fs:
			cc_data.update({line.split('\t')[0]:float(line.split('\t')[1])+0.5})
	return cc_data

def run():
	if os.path.isfile('/tmp/coo_weight.csv'):
		print 'remove previous data'
		os.remove('/tmp/coo_weight.csv')

	coo_data,rev_coo_dict = cooperation_count()
	pub_data = pub_count()
	cc_data = cite_count()

	for elem in coo_data:
		author1,author2 = elem.split('\t')
		with open('/tmp/coo_weight.csv','a+') as fs:
			if author2 in pub_data:
				fs.write(author1+'\t'+author2+'\t'+str(1.0*pub_data[author2]/rev_coo_dict[elem])+'\n')
				fs.write(author2+'\t'+author1+'\t'+str(1.0*pub_data[author1]/rev_coo_dict[elem])+'\n')
				
			else:
				fs.write(author1+'\t'+author2+'\t'+str(0.0)+'\n')
				fs.write(author2+'\t'+author1+'\t'+str(1.0*pub_data[author1]/rev_coo_dict[elem])+'\n')
	
		#print tmp,float(pub_data[tmp[0]])/rev_coo_dict[elem]
		#try:
		#	print [tmp[1],tmp[0]],float(pub_data[tmp[1]])/rev_coo_dict[elem]
		#	
		#except KeyError, e:
			
		#	print [tmp[1],tmp[0]],0.0




