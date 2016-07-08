all_paper=[]
with open('all') as fs:
    for line in fs:
        all_paper.append(line.split()[0])
all_paper = set(all_paper)

with open('../PaperReferences.txt') as fs:
    for line in fs:
        a = line.split()
        if a[0] in all_paper and a[1] in all_paper:
            f=open('ref_inacl','a+');f.write(line);f.close()
	if a[0] in all_paper or a[1] in all_paper:
            f=open('ref_outacl','a+');f.write(line);f.close()
