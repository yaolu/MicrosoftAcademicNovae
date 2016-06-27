#-*-coding:utf-8-*-
import ujson as json
import time
import urllib
import urllib2
import threading
import os
import commands  
from flask import Flask,jsonify,request,abort,render_template
import socket
import threading,Queue
import gevent
from random import randint,random
from random import shuffle
from pymongo import MongoClient
import ujson as json

now_year = 2016

client = MongoClient()
database = client.Novae_Data
Collection_Author_Search_Key = database.Author_Search_Key
Collection_Author_Detail = database.Author_Detail


AfId_AfN = {}
AfN_AfId = {}

CId_CN = {}
JId_JN = {}

FId_FN = {}
FN_FId = {}

CId_JId_top = []


def init_dict():
	global AfId_AfN,AfN_AfId,CId_CN,JId_JN,FId_FN,CId_JId_top
	text = ""
	with open("data/Af_dict") as inf:
		for line in inf.readlines():
			text+=line
	AfId_AfN = json.loads(text)
	for key,value in AfId_AfN.items():
		AfN_AfId[value] = key


	text = ""
	with open("data/Conf_dict") as inf:
		for line in inf.readlines():
			text+=line
	CId_CN = json.loads(text)
	
	text = ""
	with open("data/Jour_dict") as inf:
		for line in inf.readlines():
			text+=line
	JId_JN = json.loads(text)

	text = ""
	with open("data/Field_dict") as inf:
		for line in inf.readlines():
			text+=line
	FId_FN = json.loads(text)

	for key,value in FId_FN.items():
		FN_FId[value] = int(key)

	with open("data/top_conf_journal") as inf:
		for line in inf.readlines():
			CId_JId_top.append(int(line.split('\t')[0] ) )


app = Flask(__name__)
#@app.route('/api.chinacloudapp.cn/vvv')
@app.route('/vonae')
def init():
	return "welcome to vonae"

@app.route("/circle_test")
def test1():
	minscore, fields, pps = get_roots('pps')
	return render_template('novae_search_circle_test.html', roots = pps)


def AfN_to_AfId(AfN):
	print AfN,"AfN"
	return AfN_AfId.get(AfN, "Unknow")
	

def AfId_to_AfN(AfId):

	return AfId_AfN.get(str(AfId), "Unknow")


def FN_to_FId(FN):
	FId = FN_FId.get(FN, "Unknow")
	return FId



def FId_to_FN(FId):
	name = FId_FN.get(FId, "Unknow")
	return name

Color_l = ["rgb(51, 122, 183)", "rgb(217, 87, 79)", "rgb(91, 192, 222)",\
			"rgb(92, 184, 92)","#9400D3","#0000FF"]
def FId_to_Color(FId):
	i = hash(FId)%len(Color_l)
	return Color_l[i]


def AuId_to_PicId(AuId):
	return 10


def Academic_Year_to_Color(year):
	R,G,B = 150,255,255
	d = 0
	if year<=5:
		d = year*30
	if year>5:
		d = 150 + (year-5)*10
                  #0-50  rgb(150,255,255) - rgb(0,0,120)

	R = max(0, R-d)
	G = max(0, min(255, G-d+150) )
	B = max(120, min(255, B-d+405) )
	return "rgb(%d,%d,%d)" %(R,G,B)

def Score_to_Size(score):
	if score>=5000:
		return 20
	if score>=1000:
		return score/1000+15    #16-20
	if score >= 200:
		return score/100 + 6            # 7-15
	if score >= 0:
		return score/40 + 3       # 3-7 
	return 3

def JId_is_Top(JId):
	return int(JId) in CId_JId_top 

def CId_is_Top(CId):
	return int(CId) in CId_JId_top 

def Paper_CC_to_Size(CC):
	score = CC
	if score>=2500:
		return 18
	if score>=1000:
		return score/300+10    #13-18
	if score >= 200:
		return score/200 + 8            # 9-13 
	if score >= 50:
		return score/50 + 5                   # 6-8
	if score >= 0:
		return score/20+3                #  3-5
	return 3


def get_roots(commands):
	fields = {}
	# compile the search command use commands
	person_each_page = 24
	print commands
	search_command = {}
	page_num = commands.get("page_num", 1)
	options = commands.get("option",[])
	min_score = int(commands.get("min_score",1000000))

	command = commands.get("command","")
	if command:
		print FN_to_FId(command),"command, Field"
		search_command["field"] = str(FN_to_FId(command))
		print search_command["field"]


	search_command["score"]={"$lt":min_score}


	if options:
		options = options.split(",")
		AfN_l = []
		age_l = []
		for option in options:
			key,value = option.split(":")
			if key == "AfN":
				AfN_l.append(value.strip())
			if key == "age":
				start, end = value.split("-")
				start = int(start)
				end = int(end.strip())
				age_l.append({"$gte": now_year-end, "$lte": now_year-start})
		if AfN_l:
			search_command["now_work_for"]={"$in": [AfN_to_AfId(AfN) for AfN in AfN_l] }
		if age_l:
			search_command["$or"] = [{"start_year":age} for age in age_l]




	# select from mongodb the author search key match the commands
	Author_l = Collection_Author_Search_Key.find(search_command).sort("score",-1).limit(person_each_page)
	# use the auid to get the author detail message 
	Author_Detail_l = []
	for au in Author_l:
		min_score = min(au["score"],min_score)
		Author_Detail_l.append( (au, Collection_Author_Detail.find_one( {"AuId": au["AuId"] } ) ) ) 
		
	# compile the output json
	person_l = []
	au_num = 0
	for au_k, au_d in Author_Detail_l:
		au_num += 1
		person={}
		person["name"] = au_d["AuN"]
		person["id"] = au_d["AuId"]
		person["now"] = now_year
		person["start_year"] = au_d["start_year"]
		person["academic_year"] = now_year - person["start_year"]
		person["fields"] = [ {"message":FId_to_FN(fid[0]) ,"color":FId_to_Color(fid[0]) }  for fid in au_d["work_field"][0:3] ]

		if not person["fields"]:
			 person["fields"] = [{"message": "no_field","color":"#CCFFFF"}]

		p_history_af = au_d["history_work_for"]
		p_history_af = sorted(p_history_af.items(), key = lambda d:d[1][1] , reverse=True)[0:3]
		person["Af"] = [{"description": "%s  %d-%d"%( AfId_to_AfN(af[0]), af[1][0], af[1][1]) } for af in p_history_af ]
		person["pic_id"] = AuId_to_PicId( au_d["AuId"] )
		person["description"] = "Author: %s <br>Afflication: %s <br>Cited Num: %s" % \
										(au_d["AuN"], AfId_to_AfN( au_d["now_work_for"] ), au_d["total_CC"])
		person["color"] = Academic_Year_to_Color(person["academic_year"])
		person["size"] = Score_to_Size(au_k["score"])
		person["rr"] = 1
		person["distance"] = 1
		person["num"] = (int(page_num)-1)*person_each_page + au_num

		papers = au_d["first_au_paper"]
		children = []
		top_c = []
		normal_c = []
		for paper in papers:
			child = {}
			desc_l = []
			desc_l.append("<p>Title: " + paper[1].replace('"','\'').replace("\\","") )  # paper name
			desc_l.append("Cited Num: " + str(paper[3]))  #cited CC
			desc_l.append("Publish Year: "+ str(paper[2]))
			Top = False
			if paper[4] and paper[5]:
				desc_l.append("Publish Journal: "+paper[5])
				Top = JId_is_Top(paper[4])
			elif paper[6] and paper[7]:
				desc_l.append("Publish Conference: "+paper[7])
				Top = CId_is_Top(paper[6])
			else:
				desc_l.append("Publish Organization: Unknow")

			child["description"] = "<p>".join(desc_l)
			child["color"] = "rgb(20,255,20)" if Top else "rgb(255,20,20)"
			child["size"] = Paper_CC_to_Size(paper[3])
			child["distance"] =  1 if Top else 1/0.618
			if Top:
				top_c.append(child)
			else:
				normal_c.append(child)
		
		top_c = top_c[0: 20]
		l_t = len(top_c)
		normal_c = normal_c[0: 20 - l_t/2]
		num = 0
		for c in top_c:
			c["rr"] = (360.0/l_t*num+randint(-72/l_t, 72/l_t))/ 360.0 
			children.append(c)
			num += 1
		l_n = len(normal_c)
		num = 0
		for c in normal_c:
			c["rr"] = (360.0/l_n*num+randint(-90/l_n, 90/l_n))/ 360.0 
			children.append(c)
			num += 1

		person["children"] = children
		person_l.append(person)
		for f in person["fields"]:
			fields[f["message"]] = f

	return min_score, fields.values(), person_l


@app.route("/get_more_people", methods=["POST",])
def get_people():
	print "get_people"
	data = request.get_data()
	print type(data)
	print data
	data = json.loads(data)
	page_num = data.get("page_num")
	option = data.get("condition")
	command = data.get("command")
	min_score = data.get("min_score")
	print page_num
	print option
	print command

	commands={"min_score":min_score, "page_num":page_num, "option": option, "command":command}
	min_score, fields, roots  = get_roots(commands)
	return jsonify({"min_score":min_score ,"fields":fields,"fields_html":render_template("fields_list.html", fields=fields)\
		,"html": render_template("people_card.html", roots=roots) }) 


@app.route("/search")
def search_main():

	print "search_main"
	print request.values
	option =  request.values.getlist("s_option")
	command = request.values.get("command","")
	commands = {"min_score":1000000 ,"page_num":1, "option": option, "command":command}
	min_score, fields, roots = get_roots(commands)
	commands["min_score"] = min_score
	commands = jsonify(commands)
	return render_template("search.html", fields=fields, roots=roots, commands=commands, search_input=command, min_score=min_score)


def get_root_by_Id(AuId):
	fields = {}
	search_command={}
	# compile the search command use commands
	search_command["AuId"] = AuId

	# select from mongodb the author search key match the commands
	au_k = Collection_Author_Search_Key.find_one(search_command)
	au_d = Collection_Author_Detail.find_one( search_command )
	
	# compile the output json

	## person_message
	Author={}
	Author["name"] = au_d["AuN"]
	Author["id"] = au_d["AuId"]
	Author["now"] = now_year
	Author["start_year"] = au_d["start_year"]
	Author["academic_year"] = now_year - Author["start_year"]
	Author["fields"] = [ {"message":FId_to_FN(fid[0]) ,"color":FId_to_Color(fid[0]) }  for fid in au_d["work_field"] ]

	if not Author["fields"]:
		 Author["fields"] = [{"message": "no_field","color":"#CCFFFF"}]

	p_history_af = au_d["history_work_for"]
	p_history_af = sorted(p_history_af.items(), key = lambda d:d[1][1] , reverse=True)
	Author["Af"] = [{"description": "%s  %d-%d"%( AfId_to_AfN(af[0]), af[1][0], af[1][1]) } for af in p_history_af ]
	Author["pic_id"] = AuId_to_PicId( au_d["AuId"] )
	Author["description"] = "Author: %s <br>Afflication: %s <br>Cited Num: %s" % \
									(au_d["AuN"], AfId_to_AfN( au_d["now_work_for"] ), au_d["total_CC"])
	Author["color"] = Academic_Year_to_Color(Author["academic_year"])
	Author["size"] = Score_to_Size(au_k["score"])
	Author["rr"] = 1
	Author["distance"] = 1
	## paper children message

	papers = au_d["first_au_paper"]
	children = []
	top_c = []
	normal_c = []
	for paper in papers:
		child = {}
		desc_l = []
		desc_l.append("<p>Title: " + paper[1].replace('"','\'').replace("\\","") )  # paper name
		desc_l.append("Cited Num: " + str(paper[3]))  #cited CC
		desc_l.append("Publish Year: "+ str(paper[2]))
		Top = False
		if paper[4]:
			desc_l.append("Publish Journal: "+paper[5])
			Top = JId_is_Top(paper[4])
		elif paper[6]:
			desc_l.append("Publish Conference: "+paper[7])
			Top = CId_is_Top(paper[6])
		else:
			desc_l.append("Publish Organization: Unknow")

		child["description"] = "<p>".join(desc_l)
		child["color"] = "rgb(20,255,20)" if Top else "rgb(255,20,20)"
		child["size"] = Paper_CC_to_Size(paper[3])
		child["distance"] =  1 if Top else 1/0.618
		if Top:
			top_c.append(child)
		else:
			normal_c.append(child)

	l_t = len(top_c)
	num = 0
	for c in top_c:
		c["rr"] = (360.0/l_t*num+randint(-72/l_t, 72/l_t))/ 360.0 
		children.append(c)
		num += 1
	l_n = len(normal_c)
	num = 0
	for c in normal_c:
		c["rr"] = (360.0/l_n*num+randint(-90/l_n, 90/l_n))/ 360.0 
		children.append(c)
		num += 1

	Author["children"] = children


	## work_together 
	work_together_dict = au_d["work_together"]
	work_together = sorted(work_together_dict.items(), key=lambda d:d[1], reverse=True)
	show_work =[ int(key) for key,value in work_together[0:3]]

	### max_work
	AuId_l =[int(key) for key in au_d["work_together"].keys()]

	search_command = {"AuId":{"$in": AuId_l} }

	score_max_work_together = Collection_Author_Search_Key.find(search_command).limit(5)
	score_max_AuId_l = []
	for au in score_max_work_together:
		score_max_AuId_l.append(int( au["AuId"]) )

	### total work
	AuId_l = score_max_AuId_l + show_work
	AuId_l = list(set(AuId_l))

	search_command = {"AuId": {"$in": AuId_l} } 
	au_k = [ au for au in Collection_Author_Search_Key.find(search_command).sort("AuId") ]
	au_d = [ au for au in Collection_Author_Detail.find(search_command).sort("AuId") ]
	
	Author_l = []
	for au_k, au_d in zip(au_k, au_d):
		person = {}
		person["id"] = au_d["AuId"]
		person["academic_year"] = now_year - au_d["start_year"]
		person["color"] = Academic_Year_to_Color(person["academic_year"])
		person["size"] = Score_to_Size(au_k["score"])
		person["distance"] = 3
		papers = au_d["first_au_paper"]
		top_n = 0
		normal_n = 0
		for paper in papers:
			Top = False
			if paper[4]:
				Top = JId_is_Top(paper[4])
			elif paper[6]:
				Top = CId_is_Top(paper[6])
			if Top:
				top_n += 1
			else:
				normal_n += 1

		person["top_num"] = top_n
		person["normal_num"] = normal_n
		person["together_num"] = work_together_dict[ str(au_k["AuId"]) ]


		person["description"] = "Author: %s <br>Afflication: %s <br>Cited Num: %s<br>Work Together: %s Times<br>Top_Paper_num: %s<br>Normal_Paper_num: %s" % \
			(au_d["AuN"], AfId_to_AfN( au_d["now_work_for"] ), au_d["total_CC"], work_together_dict[ str(au_k["AuId"]) ], top_n, normal_n)
		


		Author_l.append(person)

	a_l = len(Author_l)
	for i in range(a_l):
		Author_l[i]["rr"] = (360.0/a_l*i+randint(-90/a_l, 90/a_l))/ 360.0 

	Author["work_together"] = Author_l
	print Author["children"]
	return Author["fields"], Author


@app.route("/detail/<int:pid>")
def require_detail(pid):
	fields, Author = get_root_by_Id(pid)

	return render_template("Person_Detail.html",root=Author, fields=fields)




if __name__ =='__main__':
	init_dict()
	app.run(host='0.0.0.0',port=5000, debug=False)
	
