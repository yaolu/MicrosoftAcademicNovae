import networkx as nx

 
G = nx.read_edgelist('cooperation.csv')
def readDict(filename, sep):
        with open(filename, "r") as f:
            dict={}
            for line in f:
                    values = line.strip('\n').split(sep)
                    dict.update({values[0]:float(values[2])})
        return(dict)
readDict('quality.csv','\t')
node = readDict('quality.csv','\t')
A=nx.pagerank(G,personalization=node)


import heapq
def dict_nlargest(d,n):
        return heapq.nlargest(n ,d, key = lambda k: d[k])
name = {}
with open('namedict.txt') as fs:
    for line in fs:
        tmp = line.strip('\n').split('\t')
        name.update({tmp[0]:tmp[1]})
for elem in dict_nlargest(A,100):
    print name[elem]
