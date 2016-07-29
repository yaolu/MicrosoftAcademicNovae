import numpy as np
dict_2005 = {}
dict_2010 = {}
def readDict(filename, sep):
            with open(filename, "r") as f:
                    dict={}
                    for line in f:
                                values = line.strip('\n').split(sep)
                                dict.update({values[0]:float(values[1])})
            return(dict)
dict_2005 = readDict('author_cite_count_2005.txt','\t')
dict_2010 = readDict('author_cite_count_2010.txt','\t')
author_rank=np.loadtxt('opt_2005',dtype=str)

for i in range(1,len(author_rank),10):
	author_rank_sub = author_rank[0:i]
	cite_2005 = []
	cite_2010 = [] 
	for elem in author_rank_sub:
		try:
			cite_2005.append(dict_2005[elem])
			cite_2010.append(dict_2010[elem])
		except KeyError as e:
			pass
			
	print i,'\t',np.average(cite_2005),np.average(cite_2010)
