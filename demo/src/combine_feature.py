data=[]
with open('../result/loss.txt') as fs:
    for line in fs:
        data.append(line.strip('\n').split('\t'))

ds={}
with open('../result/quality.txt') as fs:
    for line in fs:
        tmp = line.split()
        ds.update({tmp[0]:tmp[1]})

#print ds

p = []
for elem in data:
    try:
    	#print ds[elem[0]]

        p.append([elem,ds[elem[0]]])
    except KeyError, e:
        pass

#print p
for elem in p:
	#print elem
	with open('../result/feature.txt','a+') as fs:
		fs.write('\t'.join(elem[0])+'\t'+elem[1]+'\n')
    
