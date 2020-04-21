import sys
import re
import json
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
import pickle
from sklearn import preprocessing
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
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
		li += 1
		#print(li)
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')
			arr = np.zeros((2*(words_len+tags_len+chunk_tags_len)))

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')
			a3 = line1[2].split(' ')

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
				column.append(tags.index('ROOT'))
				column.append(chunk_tags.index('ROOT'))
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


			Y.append(a3[1])

X = csr_matrix((data, (row, column)))

loaded_model = pickle.load(open('finalised_model.sav', 'rb'))
z = loaded_model.predict(X)
z_one=preprocessing.label_binarize(z, classes=['L','R','U'])
Y_one=preprocessing.label_binarize(Y, classes=['L','R','U'])
k=precision_recall_fscore_support(Y,z,average='macro')
k2=confusion_matrix(Y,z)
k3=average_precision_score(Y_one,z_one)
k4=recall_score(Y_one, z_one, average='weighted')
k5=f1_score(Y,z, average='micro')
out_L=0
out_R=0
out_U=0
inp_L=0
inp_R=0
inp_U=0
for i in z:
	if i=='L':
		out_L+=1
	elif i=='R':
		out_R+=1
	elif i=='U':
		out_U+=1
for i in Y:
	if i=='L':
		inp_L+=1
	elif i=='R':
		inp_R+=1
	elif i=='U':
		inp_U+=1

print(inp_L)
print(inp_R)
print(inp_U)
print(out_L)
print(out_R)
print(out_U)
#print(k5)

#print(Y)
#print(len(z))

cnt = 0
for i in range(len(Y)):
	if(Y[i] != z[i]):
		cnt += 1

#print(cnt)		