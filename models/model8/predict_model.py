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
psps = data['psp']

words_len = len(data['words'])
tags_len = len(data['tags'])
psps_len = len(data['psp'])

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
			arr = np.zeros((2*(words_len+tags_len+psps_len)))

			a1 = line1[0].split(' ')
			a2 = line1[1].split(' ')
			a3 = line1[2].split(' ')
			a4 = line1[3].strip()

			if a3[1] != 'U':
				li += 1
				# print(li)

				if(a1[0] == 'H'):
					row.append(li -1)
					row.append(li -1)
					row.append(li -1)
					column.append(words.index(a1[1]))
					column.append(tags.index(a1[4]) + len(words))
					column.append(psps.index(a1[8]) + len(words) + len(tags))
					data.append(1)
					data.append(1)
					data.append(1)

				elif(a1[0] == 'ROOT'):
					row.append(li -1)
					row.append(li -1)
					row.append(li -1)
					column.append(words.index('ROOT'))
					column.append(tags.index('ROOT') + len(words))
					column.append(psps.index('NULL') + len(words) + len(tags))
					data.append(1)
					data.append(1)
					data.append(1)

				z = len(words) + len(tags) + len(psps)
				row.append(li -1)
				row.append(li -1)
				row.append(li -1)
				column.append(z + words.index(a2[2]))
				column.append(z + tags.index(a2[5]) + len(words))
				column.append(z + psps.index(a2[9]) + len(words) + len(tags))
				data.append(1)
				data.append(1)
				data.append(1)


				Y.append(a4)

X = csr_matrix((data, (row, column)) , shape=(li,2*(words_len+tags_len+psps_len)))


loaded_model = pickle.load(open('finalised_model.sav', 'rb'))
z = loaded_model.predict(X)

print(len(Y))

cnt = 0
for i in range(len(Y)):
	if(Y[i] != z[i]):
		cnt += 1

print(cnt)		