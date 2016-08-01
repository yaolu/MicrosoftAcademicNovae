#!/usr/local/python
import os
import numpy as np
from collections import Counter
from scipy.stats import logistic
import coo_weight

if os.path.isfile('/tmp/quality_pubrank.csv'):
	os.remove('/tmp/quality_pubrank.csv')

def get_year_pub(author,year):

	data = []
	with open('../process_data/author_conf/'+author) as fs:
		for line in fs:
			tmp = line.strip('\n').split('\t')
			if int(tmp[2])<=year:
				data.append(tmp)
	return data

def get_author_list():
	return os.listdir('../process_data/author_conf/')

def get_top_conf():
	top_conf_set = []
	with open('../../data/top_conf_journal.txt') as fs:
		for line in fs:
			top_conf_set.append(line.strip('\n').split('\t')[1])
	return set(top_conf_set)

def main(year):
	authors = get_author_list()
	top_conf_set = get_top_conf()
	qua = {}
	for author in authors:
		data = get_year_pub(author= author, year=2005)
		total = len(data)+0.01
		count = 0
		for elem in data:
			if elem[1] in top_conf_set:
				count+=1
		qua.update({author:1.0*count/total})

	with open('/tmp/quality_pubrank.csv','a+') as fs:
		for key in qua:
			fs.write(key+'\t'+str(qua[key])+'\n')





if __name__ == '__main__':
	main(2005)
	#coo_weight.run()
	#for y in range(1980,2017):
	#	main(y)
	#	print y,'\t',os.system('python /Users/alex/Documents/MicrosoftAcademicNovae/demo/nlp/process_data/algo_data/rank.py')
	#	print '=============='
