#!/usr/bin/python

with open('paper_author') as fs:
	for line in fs:
		linedata = line.split()	
		paperid = linedata[0]
		authorid = linedata[1]
		author_number = linedata[-1]
		with open('paper_order/'+paperid,'a+') as output:
			output.write(author_number+'\t'+authorid+'\n')
