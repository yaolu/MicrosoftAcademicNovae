""" input: year
	
	output file: ../data/AuId_l_[year]
		output format:
			AuId
	
	output file: ../data/AuId_work_together_[year]
		output format:
			AuId AuId ...
	
	output file: ../data/CC_[year]
		output format:
			AuId CC_before_year
	
	output file: ../data/AuId_top_normal_[year]
		output format:
			AuId top_num normal_num total_paper_num

	output file: ../data/AuId_JId_CId_[year]
		output format:
			AuId CId/JId CId/JId ...
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
		self.CId = self.entity.get('C',{}).get('CId', '')
		self.JId = self.entity.get('J',{}).get('JId', '')
		self.AuId_l = [ str(Au.get('AuId')) for Au in self.entity.get('AA',[]) ]
		self.CJId = str(self.CId) + str(self.JId)
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
def get_entity(expr, offset=0, count=99999999):
	
	entities = []
	pe_l = []
	para = dict()
	para['attributes'] = 'Id,Y,C.CId,J.JId,AA.AuId,AA.AuN'
	para['subscription-key'] = 'f7cc29509a8443c5b3a5e56b0e38b5a6'
	para['count'] = str(count)
	para['offset'] = str(offset)
	para['expr'] = expr
	ans = get_ans(para)
	entities = json.loads(ans)['entities']

	for en in entities:
		pe = Paper_Entity(en)
		pe_l.append(pe)
	return pe_l

def get_entity_simple(expr, ):
	
	entities = []
	pe_l = []
	para = dict()
	para['attributes'] = 'Id'
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


def get_rRP_entity(paper_l, check_Y):
	expr_l = Or_expr_RId(paper_l)
	p_l = []
	for expr in expr_l:
		p_l.extend(get_entity_simple(expr="And(%s,Y<=%d)" %(expr, check_Y) ) )
	return p_l


def get_AuId_CY_CC(AuId):
	check_Y = year
	CJId_l = []
	paper_l = get_entity("And(Composite(AA.AuId=%s),Y<=%d)" % (AuId, check_Y) )
	for paper in paper_l:
		CJId_l.append(paper.CJId)
	rp_l = get_rRP_entity(paper_l, check_Y)
	CC_ans = len(rp_l)
	return AuId, CC_ans, CJId_l


def get_AuId_by_FN(FN, Y, start, end):
	paper_l = get_entity("And(Composite(F.FN='%s'),Y<=%d)" %(FN, Y) , offset=start, count=end-start)
	return [paper.AuId_l for paper in paper_l]


year = 2000
if __name__ =='__main__':
	f_AuId_l_year = open( "../data/AuId_l_%d" % year , "w")
	f_AuId_work_togethor_year = open( "../data/AuId_work_togethor_%d" % year , 'w')
	f_CC_year = open( "../data/CC_%d" % year , 'w')
	f_AuId_top_normal_year = open( "../data/AuId_top_normal_%d" % year, 'w')
	f_AuId_JId_CId_year = open( "../data/AuId_JId_CId_%d" % year ,"w")
	top_CId_JId = set()
	with open('../data/top_conf_journal' , 'r') as f_top_CId_JId:
		for line in f_top_CId_JId.readlines():
			CJId = line.split('\t')[0]
			top_CId_JId.add(CJId)

	AuId_s = set()

	process_l = []
	process_num = 500
	pool = Pool( )
	ans = []
	last_n = 0
	s = time.time()
	while True:
		args_l = []
		for i in range(last_n, last_n+process_num):
			args_l.append( ('computer science', year, i*1000, i*1000+1000) )
		last_n += process_num
		anss = []
		for args in args_l:
			anss.append( pool.apply_async(get_AuId_by_FN, args) )
		
		empty = True
		print 'l ans', len(anss)
		for ans in anss:
			ans = ans.get()
			for AuId_l in ans:
				if AuId_l:
					empty = False
				f_AuId_work_togethor_year.write( '\t'.join(AuId_l) +'\n')
				AuId_s.update(AuId_l)

		if empty:
			f_AuId_work_togethor_year.close()
			f_AuId_l_year.write('\n'.join( list(AuId_s) ) )
			f_AuId_l_year.close()
			break
		print (time.time()-s) 
	print 'stage one finish'

	print 'total Author:', len(AuId_s)

	last_n = 0
	AuId_l = list(AuId_s)
	s = time.time()
	while True:
		args_l = AuId_l[last_n: last_n+process_num]
		last_n += process_num

		if not args_l:
			break
		ans = []
		for args in args_l:
			ans.append( pool.apply_async(get_AuId_CY_CC, args=(args, ) ) )
		
		print 'l ans2', len(ans)

		for an in ans:
			AuId, CC_ans, CJId_l = an.get()
			print AuId
			f_CC_year.write( "%s\t%s\n" %(AuId, CC_ans) )
			f_AuId_JId_CId_year.writelines("%s\n%s\n" %(AuId, '\t'.join(CJId_l) ) )
			top = len( filter(lambda Id: 1 if Id in top_CId_JId else None, CJId_l) )
			total = len(CJId_l)
			normal = total - top
			f_AuId_top_normal_year.write( '\t'.join( map(str, [AuId, top, normal, total] ) )  )
			f_AuId_top_normal_year.write('\n')
		print (time.time()-s) / (last_n+1)
	f_CC_year.close()
	f_AuId_JId_CId_year.close()
	f_AuId_top_normal_year.close()




