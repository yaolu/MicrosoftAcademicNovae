
data=[]
with open('../data/AuId_Academic_net.txt','r') as fs:
    for line in fs:
        data.append(line.strip('\n').split('\t'))


top=[]
with open('../data/top_conf_journal.txt','r') as fs:
    for line in fs:
        top.append(line.strip('\n').split('\t')[0])

dd={}
for elem in data:
    dd.update({elem[0]:[0,0]})


for elem in data:
    ret = dd[elem[0]]
    if elem[3] in top:
        ret[0]+=1
    ret[1]+=1
    dd.update({elem[0]:ret})

for key in dd:
    ret = dd[key]
    if ret[1]>5:
        ratio = 1.0*ret[0]/ret[1]
        with open('../data/quality.txt','a+') as fs:
            fs.write(str(key)+'\t'+str(ratio)+'\n')
