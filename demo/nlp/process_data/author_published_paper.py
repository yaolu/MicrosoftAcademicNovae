
paper_year = open('../data/ACLPapers.txt').readlines()
paper_year = [paper.strip('\r\n').split('\t') for paper in paper_year]
paper_year_dict = {}
for paper in paper_year:
    paper_year_dict.update({paper[0]:paper[3]})


with open('paper_author') as fs:
    for line in fs:
        tmp_data = line.strip('\r\n').split('\t')
        if tmp_data[-1] == '1':
            with open('author_paper/first/'+tmp_data[1],'a+') as fs:
                fs.write(tmp_data[0]+'\t'+paper_year_dict[tmp_data[0]]+'\n')
        else:
            with open('author_paper/non-first/'+tmp_data[1],'a+') as fs:
                fs.write(tmp_data[0]+'\t'+paper_year_dict[tmp_data[0]]+'\n')



