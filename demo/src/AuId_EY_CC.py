# get Author each year cited increase.

import ujson as json
import time
import urllib
import urllib2
import os
import gevent
url = 'http://oxfordhk.azure-api.net/academic/v1.0/evaluate'
expr_max_length = 1000
para = dict()
para['attributes'] = 'Id,Y'
para['subscription-key'] = 'f7cc29509a8443c5b3a5e56b0e38b5a6'
para['count'] = '50000000'
para['offset']='0'
host = 'oxfordhk.azure-api.net'
port = 80
domain = 'academic/v1.0/evaluate'


class Paper_Entity(object):

	def __init__(self, entity):
		self.entity = entity
		self.init_PE()

	def init_PE(self):
		self.Id = self.entity.get('Id')
		self.Y = self.entity.get('Y')

	def __eq__(self, other):
		return self.Id == other.Id

	def __hash__(self):
		return hash(self.Id)



import httplib
import urllib
def get_ans(para):
	ans = 0
	src = urllib.urlencode(para)
	httpClient = httplib.HTTPConnection('oxfordhk.azure-api.net', 80)
	httpClient.request('GET', '/academic/v1.0/evaluate?%s'%(src,))
	response = httpClient.getresponse()
	ans = response.read()
	httpClient.close()
	return ans


#@profile
def get_entity(expr):
	
	entities = []
	pe_l = []
	para = dict()
	para['attributes'] = 'Id,Y'
	para['subscription-key'] = 'f7cc29509a8443c5b3a5e56b0e38b5a6'
	para['count'] = "9999999"
	para['expr'] = expr
	ans = get_ans(para)
	entities = json.loads(ans)['entities']

	for en in entities:
		pe = Paper_Entity(en)
		pe_l.append(pe)
	return pe_l


def Or_expr_RId(paper_l):
	Id_l = []
	for paper in paper_l:
		Id_l.append(paper.Id)
	ans_l = []
	length = len(Id_l)
	if not Id_l:
		return []
	ans = 'RId=%s'%(Id_l[0])
	for i in range(1, length):
		t = 'Or(%s,RId=%s)'%(ans,Id_l[i])
		if len(t)>expr_max_length:
			ans_l.append(ans)
			ans = 'RId=%s'%(Id_l[i],)
		else:
			ans = t
	ans_l.append(ans)
	return ans_l

def get_rRP_entity(paper_l):
	expr_l = Or_expr_RId(paper_l)
	p_l = []
	for expr in expr_l:
		p_l.extend(get_entity(expr))
	return p_l

def get_AuId_EY_CC(line):
	AuId = line.split('\t')[0]
	Y0 = int(line.split('\t')[2])
	paper_l = get_entity("Composite(AA.AuId=%s)" %(AuId, ) )
	rp_l = get_rRP_entity(paper_l)
	rp_s = set(rp_l)
	Y_num = {}
	for paper in rp_s:
		Y = int(paper.Y)
		Y_num[Y] = Y_num.get(Y, 0) + 1
	Y_out = []
	for Y in range(Y0, 2021):
		Y_out.append(str(Y_num.get(Y, 0)))
	
	return (line, Y_out)


if __name__ =='__main__':
	thread_l = []
	gevent_num = 20
	s = time.time() 
	i = 0
	with open('5000_CC','r') as inf:
		with open('AuId_EY_CC.txt','w') as outf:
			for line in inf.readlines():
				i += 1
				gt = gevent.spawn(get_AuId_EY_CC, line) 
				thread_l.append(gt)
				if len(thread_l)>=gevent_num:
					gevent.joinall(thread_l)
					print "average:",(time.time()-s)/i
					for t in thread_l:
						line, Y_out = t.value
						outf.write(line)
						outf.write("%s\n\n"%('\t'.join(Y_out), ))
					thread_l = []

