import os
nameList = os.listdir('paper_order/')
data=[]
a={}
for elem in nameList:
    with open('paper_order/'+elem) as fs:
        a={}
        for line in fs:
            tmp_data = line.split()
            a.update({tmp_data[0]:tmp_data[1]})
    for key in a:
        if key != '1':
            try:
                data.append([a['1'],a[key]])
            except KeyError as e:
                print 'error'
