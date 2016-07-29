f=open('ref_inacl').readlines()
f[0]
f=[elem.strip('\r\n').split('\t') for elem in f]
f[0]
ls
cd inacl/
ls
ls
cd ..
ls
cd ..
ls
more ACLPapers.txt
paper_year = open('ACLPapers.txt').readlines()
paper_year[0]
paper_year = [paper.strip('\r\n').split('\t') for paper in paper_year]
paper_year[0]
m={}
for paper in paper_year:
    m.update({paper[0]:int(paper[3])})
paper_year = m
paper_year
ls
cd PaperReferences/inacl/
ls
for elem in f:
    with open(elem[1],'a+') as fs:
        fs.write(elem[0]+'\t'+str(paper_year[elem[0]])+'\n')
%history -f cite_to_paper.py
