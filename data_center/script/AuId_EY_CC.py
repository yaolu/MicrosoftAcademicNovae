""" input file: AuId_Start_Y_Check_Y
		input format: AuId\t Start_Y\tCheck_Y1\tCheck_Y2....

	output file: AuId_EY_CC.txt
		output format: 
			AuId
			Check_Y1\tCheck_Y2...
			Y1_CC\tY2_CC...
			\n


"""


import ujson as json
import time
import urllib
import urllib2
import multiprocessing
from multiprocessing import Pool
import os
import gevent
url = 'http://oxfordhk.azure-api.net/academic/v1.0/evaluate'
expr_max_length = 1000
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
		break
	return p_l

def get_AuId_EY_CC(AuId, start_Y=1900, check_Y=[2005, 2016]):

	paper_l = get_entity("Composite(AA.AuId=%s)" %(AuId, ) )
	rp_l = get_rRP_entity(paper_l)
	rp_s = set(rp_l)
	Y_num = {}
	for paper in rp_s:
		Y = int(paper.Y)
		Y_num[Y] = Y_num.get(Y, 0) + 1
	ans = []
	cited_tmp = 0
	for Y in range(start_Y, max(check_Y)+1 ):
		cited_tmp += Y_num.get(Y, 0)
		if Y in check_Y:
			ans.append(str(cited_tmp))

	re={}

	return AuId, [str(Y) for Y in check_Y], ans

if __name__ =='__main__':
	process_l = []
	process_num = multiprocessing.cpu_count()*10
	s = time.time() 
	i = 0
	pool = Pool( multiprocessing.cpu_count() )
	with open('AuId_EY_CC.txt','w') as outf:
		with open('AuId_Start_Y_Check_Y','r') as inf:
			for line in inf.readlines():
				i += 1
				args = line.split('\t')
				AuId = args[0]
				start_y = int(args[1])
				check_Y = [ int(v) for v in args[2:] ]
				process_l.append( pool.apply_async(func=get_AuId_EY_CC, args=(AuId, start_y, check_Y) ) )
				if len(process_l)>=process_num:
					print "average:",(time.time()-s)/i
					for t in process_l:
						AuId, check_Y, ans = t.get()

						outf.write(AuId)
						outf.write("\n")
						outf.write("%s\n"%('\t'.join(check_Y), ))
						outf.write("%s\n\n"%('\t'.join(ans), ))
					process_l = []
		for t in process_l:
			AuId, check_Y, ans = t.get()

			outf.write(AuId)
			outf.write("\n")
			outf.write("%s\n"%('\t'.join(check_Y), ))
			outf.write("%s\n\n"%('\t'.join(ans), ))
		