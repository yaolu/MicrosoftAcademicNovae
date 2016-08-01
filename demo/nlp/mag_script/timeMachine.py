#!/usr/local/python
import os
import numpy as np
from collections import Counter
from scipy.stats import logistic
import coo_weight


################
# init all datafiles
#############
if os.path.isfile('/tmp/quality.csv'):
	os.remove('/tmp/quality.csv')
if os.path.isfile('/tmp/cooperation.csv'):
	os.remove('/tmp/cooperation.csv')

def get_worldwide_data():
	data=[]
	with open('../data/ACLPapers.txt') as fs:
		for line in fs:
			data.append(line.strip('\r\n').split('\t'))
	return data

def get_timemachine_paper(paper_data,year):
	return [paper_info for paper_info in paper_data if int(paper_info[3]) <= int(year)]


def get_timemachine_author(paper_info,write_to_file):
	all_paper = set([item[0] for item in paper_info])
	author_info = []
	with open('../data/PaperAuthorAffiliations.txt') as fs:
		for line in fs:
			a = line.strip('\r\n').split('\t')
			if a[0] in all_paper:
				if write_to_file:
					with open('/tmp/paper_author','a+') as output:
						output.write(line)
				else:
					author_info.append(line.strip('\r\n').split('\t'))
	return author_info



def generate_cooperation_info(author_info,write_to_file):

	#os.mkdir('/tmp/paper_order')
	paper2author_dict ={}
	for single_author_info in author_info:	
		[paperid, authorid, author_number] = single_author_info[0:2]+[single_author_info[-1]]
		if paperid in paper2author_dict:
			#print [paperid, authorid, author_number]
			prev_data = paper2author_dict[paperid]
			#prev_data.append()

			paper2author_dict[paperid]= prev_data+[[author_number,authorid]]
			#print paper2author_dict

		else:
			paper2author_dict[paperid]=[[author_number,authorid]]
		#print paper2author_dict

		if write_to_file:
			with open('/tmp/paper_order/'+paperid,'a+') as output:
				output.write(author_number+'\t'+authorid+'\n')
	#print paper2author_dict
	nameList = [key for key in paper2author_dict]
	coo_data=[]
	a={}
	for key in paper2author_dict:
		a={}
		tmp_data = paper2author_dict[key]
		for tmp_data_item in tmp_data:
		#print tmp_data
			a.update({tmp_data_item[0]:tmp_data_item[1]})
		for key in a:
			if key != '1':
				try:
					coo_data.append([a['1'],a[key]])
				except KeyError as e:
					pass
					#print 'keyerror,ignore'
	if write_to_file:
		with open('/tmp/cooperation.csv','a+') as output:
			for elem in coo_data:
				output.write('\t'.join(elem)+'\n')
	return(coo_data)



def pub_num_author(author_info, isfirst):
	if isfirst:
		authorlist = [item[1] for item in author_info if item[-1]=='1']
	else:
		authorlist = [item[1] for item in author_info]

	return Counter(authorlist)

def modified_logistic(x):
	return logistic.cdf(x,scale=5,loc=15)




def main(timemachine_year):
	
	#######################
	# Get the paper before a specific year 
	##########
	data = get_worldwide_data()
	data_2010 = get_timemachine_paper(data,timemachine_year)

	############################
	# Get Author information of papers before a specific year 
	###########################
	author_info_2010 = get_timemachine_author(paper_info = data_2010, write_to_file = False)
	coo_data =  generate_cooperation_info(author_info_2010,write_to_file=True)
	#print author_info_2010

	##############################
	# From author info generate cooperation
	#######################


	author_num_dict = pub_num_author(author_info_2010, isfirst = True)
	with open('/tmp/quality.csv','a+') as fs:
	        for key in author_num_dict:
	                fs.write(key+'\t'+str(author_num_dict[key])+'\t'+str(modified_logistic(author_num_dict[key]))+'\n')

if __name__ == '__main__':
	main(2016)
	coo_weight.run()
	#for y in range(1980,2017):
	#	main(y)
	#	print y,'\t',os.system('python /Users/alex/Documents/MicrosoftAcademicNovae/demo/nlp/process_data/algo_data/rank.py')
	#	print '=============='
