# clean file "computer_vision_all_raw" to file "scholar_feature"

import re
from collections import defaultdict
import operator
def unify(filename):
	f = open(filename).readlines()
	x = []
	content= []
	for i in range(len(f)-1):
		x.append(f[i])
		if f[i] == "\n" and f[i+1] == "\n":
			content.append(x)
			x = []

	paper_content = []
	for i in range(len(content)):
		y = []
		co_au = []
		for item in content[i]: 
			if "paperId" in item:
				y.append(item.strip("\n").strip("paperId: "))
			elif "AuId" in item:
				co_au.append(item.split(",")[0].strip("AuId "))
			elif "paper cited num" in item:
				y.append(item.strip("\n").strip("paper cited num: "))
			elif "paper year" in item:
				y.append(item.strip("\n").strip("paper year: "))
			elif "paper Conference" in item:
				a = item.strip("\n").strip("paper Conference and Journal ")
				conf = re.sub("None|,|N|[0-9]*","",a)
				y.append(conf)
			#else:
			#	y.append("NULL")
		y.append(co_au)
		paper_content.append(y)
	return paper_content



def top_affiliation(f_c,f_j):
	conf_file = open(f_c).readlines()
	conf = [ele.split(" ")[0].lower() for ele in conf_file]
	journal_file = open(f_j).readlines()
	journal = [ele.split(" ")[0].lower() for ele in journal_file]
	return conf,journal

def get_auth_paper_conf(paper_content):
	cited_num = [int(item[2]) for item in paper_content]
	#cited_score =  [ele*100/float((max(cited_num)-min(cited_num))) for ele in cited_num]
	auth_content = defaultdict(list)
	for i in range(len(paper_content)):
		for ele in paper_content[i][4]:
			auth_content[ele].append([cited_num[i],paper_content[i][3]])
	return auth_content


def get_auth_affi_score(auth_content,auth_id,conf,journal):
	affi = [ele[1] for ele in auth_content[auth_id]]
	affi_score = 0
	for item in affi:
		if item in conf:
			affi_score +=1
		elif item in journal:
			affi_score+=1
	affi_score = affi_score/float(len(affi))
	return affi_score


def auth_result():
	paper_content = unify("computer_vision_all_raw")
	conf,journal = top_affiliation("conference_rank_name","journal_rank_name")
	auth_content = get_auth_paper_conf(paper_content)
	auth_name = auth_content.keys()
	auth_final = dict()
	for auth_id in auth_name:
		cited_number = [ele[0] for ele in auth_content[auth_id]]
		if len(cited_number) >3:
			cited_score = sum(cited_number)/float(len(cited_number))
		else:
			#cited_score = 0.1* sum(cited_number)/float(len(cited_number)) 
			cited_score = 0
		affi_score = get_auth_affi_score(auth_content,auth_id,conf,journal)
		res = []
		res.append(cited_score)
		res.append(affi_score)
		res.append(len(cited_number))
		auth_final[auth_id] = res

	#sorted_x = sorted(auth_final.items(), key=operator.itemgetter(1))
	return auth_final








