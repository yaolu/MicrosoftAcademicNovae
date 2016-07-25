f=open('PaperAuthorAffiliations.txt').readlines()
paper_author = [elem.split('\t')[0:2] for elem in f]
author = open('AuthorsList.txt').readlines()
author = [elem.strip('\n') for elem in author]
for elem in author:
    for item in paper_author:
        if item[1]==elem:
            with open('author_pub/'+elem,'a+'):
                ff.write(item[0]+'\n')
for elem in author:
    for item in paper_author:
        if item[1]==elem:
            with open('author_pub/'+elem,'a+') as ff:
                ff.write(item[0]+'\n')
ls
head
more ACLPapers.txt
f=open('ACLPapers.txt')
f=open('ACLPapers.txt').readlines()
f=[elem.strip('\n').split('\t') for elem in f]
papers = f
paper=f
paper[0:2]
f=[elem.strip('\r\n').split('\t') for elem in f]
f=open('ACLPapers.txt').readlines()
f=[elem.strip('\r\n').split('\t') for elem in f]
paper=f
paper[0:2]
ls
import os
name = os.listdir('author_pub/')
for elem in name:
    f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        for gg in paper:
            if gg[0]==item[0]:
                with open('pub/'+elem,'a+') as fff:
                    fff.write('\t'.join(gg)+'\n')
for elem in name:
    print elem;f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        for gg in paper:
            if gg[0]==item[0]:
                with open('pub/'+elem,'a+') as fff:
                    fff.write('\t'.join(gg)+'\n')
for elem in name:
    print elem;f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        for gg in paper:
            if gg[0]==item:
                with open('pub/'+elem,'a+') as fff:
                    fff.write('\t'.join(gg)+'\n')
for elem in name:
    print elem;f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        for gg in paper:
            if gg[0]==item:
                with open('pub/'+elem,'a+') as fff:
                    fff.write('\t'.join(gg)+'\n')
gg[0]
gg[1]
paper[0]
paper[1]
paper[2]
for elem in name:
    print elem;f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        for gg in paper:
            if gg[0]==item:
                with open('pub/'+elem,'a+') as fff:
                    fff.write('\t'.join(gg)+'\n')
elem
elem
for elem in name:
    print elem;f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        for gg in paper:
            if gg[0]==item:
                with open('pub/'+elem.strip('\n'),'a+') as fff:
                    fff.write('\t'.join(gg)+'\n')
len(name)
for elem in name:
    f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        for gg in paper:
            if gg[0]==item:
                with open('pub/'+elem.strip('\n'),'a+') as fff:
                    fff.write('\t'.join(gg)+'\n')
gg
s={}
for elem in paper:
    s.update({elem[0]:'\t'.join(elem[1:])})
gg[0] in paper
gg[0] in s
for elem in name:
    f=open('author_pub/'+elem).readlines()
    f=[elem.strip('\n') for elem in f]
    for item in f:
        with open('pub/'+elem.strip('\n'),'a+') as fff:
            fff.write(item+'\t'+s[item]+'\n')
len(data)
len(name)
for elem in name:
    f=open('author_pub/'+elem).readlines()
    f=[pp.strip('\n') for pp in f]
    for item in f:
        with open('pub/'+elem.strip('\n'),'a+') as fff:
            fff.write(item+'\t'+s[item]+'\n')
for elem in name:
    f=open('author_pub/'+elem).readlines()
    f=[pp.strip('\n') for pp in f]
    for item in f:
        with open('pub/'+elem.strip('\n'),'a+') as fff:
            fff.write(item+'\t'+s[item]+'\n')
%history -f extract_author_to_paper_info.py
