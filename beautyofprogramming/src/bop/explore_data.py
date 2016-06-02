import re
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


#dd = unify('computer_vision_file_10M')
#print dd[0]
#for elem in dd:
if __name__ == '__main__':
	dd = unify('computer_vision_all')
	for elem in dd:
		f=open('author/'+elem[4][0],'a+')
		f.write('\t'.join(elem[0:4])+'\n')
		f.close()
