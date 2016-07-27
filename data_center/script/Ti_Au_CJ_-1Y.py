""" input file: AuId_Start_Y_Check_Y
		input format: AuId\t Start_Y\tCheck_Y1\tCheck_Y2....

	output file: AuId_EY_CC.txt
		output format: 
			AuId
			Check_Y1\tCheck_Y2...
			Y1_CC\tY2_CC...
			\n


"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
		self.Ti = self.entity.get('Ti')
		self.AA = self.entity.get('AA')
		self.C = self.entity.get('C', {})
		self.J = self.entity.get('J', {})
		self.CJ = self.C.get('CN','') + self.J.get('JN','')
		self.AuN = []
		for Au in self.AA:
			self.AuN.append(Au.get('AuN'))
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
def get_entity(expr, count=999999, offset=0):
	
	entities = []
	pe_l = []
	para = dict()
	para['count'] = count
	para['offset'] = offset
	para['attributes'] = 'Id,Y,Ti,AA.AuN,C.CN,J.JN'
	para['subscription-key'] = 'f7cc29509a8443c5b3a5e56b0e38b5a6'

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

def get_abnormal_paper(count=1, offset=0):

	paper_l = get_entity("Composite(F.FN='computer vision')" , count=count, offset=offset )
	rp_l = get_rRP_entity(paper_l)
	rp_s = set(rp_l)
	Y_num = {}
	for paper in rp_s:
		Y = int(paper.Y)
		Y_num[Y] = Y_num.get(Y, 0) + 1
	ans = []
	cited_tmp = 0
	paper = paper_l[0]
	minY = min(Y_num.keys())
	if len(paper_l) and  minY >= int(paper.Y):
		return []
	else:
		paper = paper_l[0]
		return [paper.Ti, '\t'.join(paper.AuN), paper.CJ, str(Y_num.get(minY, 0))]

if __name__ =='__main__':
	process_l = []
	process_num = multiprocessing.cpu_count()*10
	s = time.time() 
	i = 0
	limit = 100
	pool = Pool( multiprocessing.cpu_count() )
	with open('../data/Ti_Au_CJ_-1Y_CC_100.txt','w') as outf:
		total = 0
		count = 0
		while total < limit:
			process_l.append( pool.apply_async(func=get_abnormal_paper, args=(1, count*1) ) )
			count += 1
			if len(process_l)>=process_num:
				for t in process_l:
					ans = t.get()
					if ans:
						Ti, Au, CJ ,bCC= ans
						outf.write( '\n'.join( [Ti, Au, CJ, bCC] ) )
						outf.write("\n\n")
						total += 1
						print total, count
				process_l = []
			