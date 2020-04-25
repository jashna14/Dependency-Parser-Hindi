import sys
import re
import json
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
import pickle

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
		li += 1
		# print(li)
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')
			a3 = line1[2].split(' ')

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


			Y.append(a3[1])

X = csr_matrix((data, (row, column)) , shape=(li, 2*(words_len+tags_len)))

loaded_model = pickle.load(open('finalised_model.sav', 'rb'))
z = loaded_model.predict(X)


iu = 0
pu = 0
il = 0
pl = 0
ir = 0
pr = 0
cnt = 0
for i in range(len(Y)):
	if(Y[i] == 'L'):
		il +=1
	if(Y[i] == 'R'):
		ir +=1
	if(Y[i] == 'U'):
		iu +=1		
	if(Y[i] != z[i]):
		if(Y[i] == 'L'):
			pl +=1
		if(Y[i] == 'R'):
			pr +=1
		if(Y[i] == 'U'):
			pu +=1
		cnt += 1

print('*****************')
print(cnt/len(Y))
print('*****************')
print(pl/il)
print('*****************')
print(pr/ir)
print('*****************')
print(pu/iu)
