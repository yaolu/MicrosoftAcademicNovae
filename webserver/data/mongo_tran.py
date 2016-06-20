#-*-coding:utf-8-*-
from pymongo import MongoClient
from ujson import loads
from time import time
client = MongoClient()
db = client.Novae_Data
collection_Author_Search_Key = db.Author_Search_Key
collection_Author_Detail = db.Author_Detail
au_l = []
i = 0

s = time()
multi_insert = []
with open("head_10000", 'r') as inf:
	collection_Author_Detail.create_index("AuId",unique=True)
	collection_Author_Search_Key.create_index("AuId",unique=True)
	collection_Author_Search_Key.create_index("score")

	bulkkeyop = collection_Author_Search_Key.initialize_ordered_bulk_op()
	bulkdetailop = collection_Author_Detail.initialize_ordered_bulk_op()

	for line in inf:
		i += 1
		au = loads(line)
		search_key = {}
		search_key["AuId"] = int(au["AuId"])
		search_key["AuN"] = au['AuN']
		search_key['start_year'] = int(au["start_year"])
		search_key["score"] = int(au["total_CC"])
		search_key["now_work_for"] = au['now_work_for']
		field = au['work_field']
		field = sorted(field.items(), key = lambda d:d[1] , reverse=True)
		au["first_au_paper"] = sorted(au["first_au_paper"], key= lambda d:d[3], reverse=True)
		au['work_field'] = field
		
		search_key['field'] = []
		for f,v in field:
			search_key['field'].append(f)
			if len(search_key['field']) >=5:
				break
		bulkkeyop.insert(search_key)
		bulkdetailop.insert(au)
		
		#collection_Author_Search_Key.update({"AuId":au["AuId"]}, search_key,True)
		#collection_Author_Detail.update({"AuId":au["AuId"]}, au, True)
		print i
		print time()-s
		s = time()																																																 
	print bulkkeyop.execute()
	print bulkdetailop.execute()





