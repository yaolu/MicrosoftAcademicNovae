import networkx as nx
import heapq
import os

#import ../../mag_script/timeMachine
def readDict(filename, sep):
        with open(filename, "r") as f:
            dict={}
            for line in f:
                    values = line.strip('\n').split(sep)
                    dict.update({values[0]:float(values[1])})
        return(dict)

def build_network(first_author,coo_filepath,quality_filepath,isweight):
	if isweight:
		G = nx.read_edgelist(coo_filepath,create_using=nx.DiGraph(),nodetype=str, data=(('weight',float),))
	else:
		G = nx.read_edgelist(coo_filepath)	
	if first_author:
		node = readDict(quality_filepath,'\t')
	else:
		node = readDict(quality_filepath,'\t')
	with open('/Users/alex/Documents/MicrosoftAcademicNovae/demo/nlp/process_data/authorlist.csv') as fs:
		for line in fs:
			try:
				tmp_data = line.strip('\n')
				node[tmp_data]
			except KeyError as e:
				node.update({tmp_data:0.0})
	A=nx.pagerank(G,personalization=node)
	return A


def dict_nlargest(d,n):
        return heapq.nlargest(n ,d, key = lambda k: d[k])



def build_namedict():
	name = {}
	with open('/Users/alex/Documents/MicrosoftAcademicNovae/demo/nlp/process_data/algo_data/author_name_age.csv') as fs:
		for line in fs:
			tmp = line.strip('\n').split('\t')
			name.update({tmp[0]:[tmp[1],int(tmp[2])]})
	return name



if __name__ == "__main__":
	A = build_network(first_author=True,coo_filepath = '/tmp/coo_weight.csv',quality_filepath='/tmp/quality.csv',isweight=True)
	name = build_namedict()
	count = 0
	if os.path.isfile('/tmp/rank_2005'):
		os.remove('/tmp/rank_2005')
	if os.path.isfile('/tmp/rank_2005_name'):
		os.remove('/tmp/rank_2005_name')
	for elem in dict_nlargest(A,2000):
		count+=1
		#if elem == '13B7FEAA':
		#	print count,elem,name[elem]
		if name[elem][1] <= 2016 and name[elem][1]>=2012:
			with open('/tmp/rank_2005','a+') as fs:
				fs.write(elem+'\n')
			with open('/tmp/rank_2005_name','a+') as fs:
				fs.write(str(count)+'\t'+elem+'\t'+str(name[elem])+'\n')			
			print count,elem,name[elem]

			
