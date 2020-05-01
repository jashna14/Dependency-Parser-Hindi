import sys
import re
import json
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
import pickle
from sklearn import preprocessing
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


def metric_analysis(k,Y,z):
	if k==0:
		ans=recall_score(Y, z, average='macro')
	elif k==1:
		ans=recall_score(Y, z, average='micro')
	elif k==2:
		ans=recall_score(Y, z, average='weighted')

	elif k==3:
		ans=f1_score(Y,z, average='macro')
	elif k==4:
		ans=f1_score(Y,z, average='micro')
	elif k==5:
		ans=f1_score(Y,z, average='weighted')

	elif k==6:
		ans=precision_score(Y,z, average='macro')
	elif k==7:
		ans=precision_score(Y,z, average='micro')
	elif k==8:
		ans=precision_score(Y,z, average='weighted')

	elif k==9:
		ans=confusion_matrix(Y,z)

	return ans


with open('data_lists.json','r') as f:
	data = json.load(f)

words = data['words']
tags = data['tags']
chunk_tags = data['chunk_tags']	

words_len = len(data['words'])
tags_len = len(data['tags'])
chunk_tags_len = len(data['chunk_tags'])

row = []
column = []
data = []

Y = []

# arr.astype(int)
# 0 1 2 3 4 5 0 1 2 3 4   0  1   2  3  4
# 0 1 2 3 4 5 6 7 8 9 10 11  12 13 14  15

""" words + tags + chunk_tags + word + tags +  chunk_tags """

li = 0
with open(sys.argv[1], 'r') as f:
	for line in f:
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')
			a3 = line1[2].split(' ')
			a4=line1[3].strip()

			if a3[1] != 'U':
				li += 1
				#print(li)

				if(a1[0] == 'H'):
					row.append(li -1)
					row.append(li -1)
					row.append(li -1)
					column.append(words.index(a1[1]))
					column.append(tags.index(a1[4]) + len(words))
					column.append(chunk_tags.index(a1[3]) + len(words) + len(tags))
					data.append(1)
					data.append(1)
					data.append(1)

				elif(a1[0] == 'ROOT'):
					row.append(li -1)
					row.append(li -1)
					row.append(li -1)
					column.append(words.index('ROOT'))
					column.append(tags.index('ROOT') + len(words))
					column.append(chunk_tags.index('ROOT') + len(words) + len(tags))
					data.append(1)
					data.append(1)
					data.append(1)

				z = len(words) + len(tags) + len(chunk_tags)
				row.append(li -1)
				row.append(li -1)
				row.append(li -1)
				column.append(z + words.index(a2[2]))
				column.append(z + tags.index(a2[5]) + len(words))
				column.append(z + chunk_tags.index(a2[4]) + len(words) + len(tags))
				data.append(1)
				data.append(1)
				data.append(1)


				Y.append(a4)

X = csr_matrix((data, (row, column)) , shape=(li,2*(words_len+tags_len+chunk_tags_len)))


loaded_model = pickle.load(open('finalised_model.sav', 'rb'))
z = loaded_model.predict(X)

print(len(Y))
cnt = 0
for i in range(len(Y)):
	if(Y[i] != z[i]):
		cnt += 1

print(cnt)		


# for i in range(10):
# 	answer=metric_analysis(i,Y,z)
# 	print(answer)
cnt = 0
for i in range(len(Y)):
	if(Y[i] != z[i]):
		cnt += 1

print(((len(Y)-cnt)/len(Y))*100)