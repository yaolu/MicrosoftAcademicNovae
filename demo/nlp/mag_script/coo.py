#!/usr/bin/python
import numpy as np
import os

namelist = os.listdir('paper_order/')
for name in namelist:
	data = np.loadtxt('paper_order/'+name,dtype='str')
	srt = np.array(sorted(data, key=lambda x:x[0]))
#	print type(srt[0])
	with open('coo.txt','a+') as output:
		if type(srt[0]) == np.ndarray:
			output.write('\t'.join(srt[:,1])+'\n')
		else:
			output.write(srt[1]+'\n')

