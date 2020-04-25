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
		print(li)
		if(line.rstrip()):
			line = re.sub('\s+',' ',line)
			line1 = line.split(';')
			arr = np.zeros((2*(words_len+tags_len)))

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

X = csr_matrix((data, (row, column)))
clf = LinearSVC()
clf.fit(X, Y)

pickle.dump(clf, open('finalised_model.sav', 'wb'))