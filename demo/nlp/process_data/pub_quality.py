import numpy as np
from scipy.stats import logistic
def softmax(x):
	"""Compute softmax values for each sets of scores in x."""
	return np.exp(x) / np.sum(np.exp(x), axis=0)

def modified_logistic(x):
	return logistic.cdf(x,scale=5,loc=15)

f=open('pub_number.csv').readlines()
data=[elem.strip('\n').split('\t') for elem in f]

output = []
for elem in data:
	output.append([elem[0],str(elem[1]),str(modified_logistic(int(elem[1])))])

with open('quality.csv','a+') as fs:
	for item in output:
		fs.write('\t'.join(item)+'\n')


