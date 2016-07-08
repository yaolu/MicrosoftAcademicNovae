all_paper=[]
with open('all') as fs:
    for line in fs:
        all_paper.append(line.split()[0])
all_paper = set(all_paper)

with open('../PaperAuthorAffiliations.txt') as fs:
    for line in fs:
        a = line.split()
        if a[0] in all_paper:
		f=open('paper_author','a+');f.write(line);f.close()
