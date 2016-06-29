from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import  DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import cross_validation
from sklearn.decomposition import PCA
from collections import Counter
from random import shuffle
a=[]
with open('../result/feature.txt') as fs:
    for line in fs:
         a.append(line.split())

famous=[]
with open('../data/1w_cc_1995_2000') as fs:
    for line in fs:
         famous.append(line.split()[0])


dataset=[]
for elem in a:
    if int(elem[2])<2001 and int(elem[2])>=1995:
        tmp=[]
        print elem
        if elem[0] in famous:
            tmp.append(map(float,[elem[1],elem[3],elem[4]]))
            #tmp.append(map(float,[elem[1],elem[4]]))
            #tmp.append(map(float,[elem[4]]))
            tmp.append('famous')
        else:
            #tmp.append(map(float,[elem[4]]))
            tmp.append(map(float,[elem[1],elem[3],elem[4]]))
            #tmp.append(map(float,[elem[1],elem[4]]))
            tmp.append('normal')
        dataset.append(tmp)
#print dataset

shuffle(dataset)
print dataset[0:5]
clf = RandomForestClassifier(n_jobs=-1)
#clf = DecisionTreeClassifier()
#skpca = PCA(n_components=1)
value = [elem[0] for elem in dataset]
#value = skpca.fit_transform(value)
print value[0:10]
label = [elem[1] for elem in dataset]
#with open('/tmp/aa.txt','a+') as fs:
#    for i in range(len(value)):
#        fs.write(str(value[i][0])+'\t'+label[i]+'\n')
value_train, value_test, label_train, label_test = cross_validation.train_test_split(value, label, test_size=0.3)
sv = SVC()
clf.fit(value_train,label_train)
print classification_report(label_test,clf.predict(value_test))
print confusion_matrix(label_test,clf.predict(value_test))
for aa,bb in zip(value,label):
	if bb =='famous':
		print aa,bb
#print cross_validation.cross_val_score(sv,value,label,cv=5)
