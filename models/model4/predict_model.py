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

with open('data_lists.json','r') as f:
	data = json.load(f)

words = data['words']
tags = data['tags']

words_len = len(data['words'])
tags_len = len(data['tags'])

row = []
column = []
data = []

Y = []

li = 0
with open(sys.argv[1], 'r') as f:
	for line in f:
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')
			arr = np.zeros((2*(words_len+tags_len)))

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')
			a3 = line1[2].split(' ')
			a4 = line1[3].strip()

			if a3[1] != 'U':
				li += 1
				#print(li)

				if(a1[0] == 'H'):
					row.append(li -1)
					row.append(li -1)
					column.append(words.index(a1[1]))
					column.append(tags.index(a1[4]) + len(words))
					data.append(1)
					data.append(1)

				elif(a1[0] == 'ROOT'):
					row.append(li -1)
					row.append(li -1)
					column.append(words.index('ROOT'))
					column.append(tags.index('ROOT') + len(words))
					data.append(1)
					data.append(1)

				z = len(words) + len(tags)
				row.append(li -1)
				row.append(li -1)
				column.append(z + words.index(a2[2]))
				column.append(z + tags.index(a2[5]) + len(words))
				data.append(1)
				data.append(1)


				Y.append(a4)

X = csr_matrix((data, (row, column)))

loaded_model = pickle.load(open('finalised_model.sav', 'rb'))
z = loaded_model.predict(X)
# k=precision_recall_fscore_support(Y,z,average='macro')
#k2=confusion_matrix(Y,z)
#k3=precision_score(Y,z,average='macro')
k4=recall_score(Y, z, average='weighted')
#k5=f1_score(Y,z, average='micro')
# out_L=0
# out_R=0
# out_U=0
# inp_L=0
# inp_R=0
# inp_U=0
# for i in z:
# 	if i=='L':
# 		out_L+=1
# 	elif i=='R':
# 		out_R+=1
# 	elif i=='U':
# 		out_U+=1
# for i in Y:
# 	if i=='L':
# 		inp_L+=1
# 	elif i=='R':
# 		inp_R+=1
# 	elif i=='U':
# 		inp_U+=1

# print(inp_L)
# print(inp_R)
# print(inp_U)
# print(out_L)
# print(out_R)
# print(out_U)
print(k4)

#print(Y)
#print(len(z))

cnt = 0
for i in range(len(z)):
	if(Y[i] != z[i]):
		cnt += 1

print(cnt)
#https://docs.google.com/document/d/1BDMr4DNS91t099pqqdVlJc2wgO75_djM_nMaXM9bdVg/edit#	