import networkx as nx
import heapq
 
def readDict(filename, sep):
        with open(filename, "r") as f:
            dict={}
            for line in f:
                    values = line.strip('\n').split(sep)
                    dict.update({values[0]:float(values[2])})
        return(dict)

def build_network(first_author):
	G = nx.read_edgelist('../cooperation.csv')
	if first_author:
		node = readDict('quality_first_author.csv','\t')
	else:
		node = readDict('quality.csv','\t')
	with open('../authorlist.csv') as fs:
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
	with open('author_name_age.csv') as fs:
		for line in fs:
			tmp = line.strip('\n').split('\t')
			name.update({tmp[0]:[tmp[1],int(tmp[2])]})
	return name



if __name__ == "__main__":
	A = build_network(first_author=True)
	name = build_namedict()
	count = 1
	for elem in dict_nlargest(A,500):
		if name[elem][1] < 2010 and name[elem][1]>2005:
			print count,elem,name[elem]
			count+=1
