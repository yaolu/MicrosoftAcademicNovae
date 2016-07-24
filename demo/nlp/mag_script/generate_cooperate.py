#!/usr/bin/python
import os
with open('../data/PaperAuthorAffiliations.txt') as fs:
	for line in fs:
		linedata = line.split()	
		paperid = linedata[0]
		authorid = linedata[1]
		author_number = linedata[-1]
		with open('paper_order/'+paperid,'a+') as output:
			output.write(author_number+'\t'+authorid+'\n')

nameList = os.listdir('paper_order/')
data=[]
a={}
for elem in nameList:
    with open('paper_order/'+elem) as fs:
        a={}
        for line in fs:
            tmp_data = line.split()
            a.update({tmp_data[0]:tmp_data[1]})
    for key in a:
        if key != '1':
            try:
                data.append([a['1'],a[key]])
            except KeyError as e:
                print 'keyerror,ignore'

with open('../process_data/cooperation.csv','a+') as output:
	for elem in data:
		output.write('\t'.join(elem)+'\n')
