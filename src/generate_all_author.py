f=open('computer_vision_all').readlines()
AA=[]
for elem in f:
    if elem[0:4]=='AuId':
        AA.append(elem)

BB=[]
for elem in AA:
    BB.append(elem.split(','))

CC=[]

for elem in BB:
    CC.append(elem[0].split(' '))

DD=[elem[1] for elem in CC]
#print DD
DD=set(DD)
DD=list(DD)

out = open('all_id_2.txt','a+')
for elem in DD:
	out.write(elem+'\n')
out.close()
