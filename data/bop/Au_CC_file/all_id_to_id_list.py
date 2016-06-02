f=open('all_cite.txt').readlines()
f[0]
dd = [elem.strip('\n').split('  ') for elem in f]
dd[0]
data=[]
for elem in data:
    data.append([elem[0].split(' ')[1],elem[1].split(' ')[1]])
data[0]
for elem in dd:
    data.append([elem[0].split(' ')[1],elem[1].split(' ')[1]])
data[0]
data[1]
data[2]
ls
ff=open('aa.txt','a+')
for elem in data:
    ff.write('\t'.join(elem)+'\n')
ff.close()
%history -f all_id_to_id_list.py
