import numpy as np
import os

def cal_age(fs):
	data = open(fs).readlines()
	data=[elem.strip('\n').split('\t') for elem in data]
	year = [int(elem[3]) for elem in data]
	return np.min(year)


namelist = os.listdir('pub/')
out = []
for elem in namelist:
	out.append([elem,cal_age('pub/'+elem)])


with open('author_age.csv','a+') as fs:
	for elem in out:
		fs.write(elem[0]+'\t'+str(elem[1])+'\n')
