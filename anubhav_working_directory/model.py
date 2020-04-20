import sys
import re
import json
import numpy as np
from scipy.sparse import csr_matrix
from scikits.learn.svm.sparse import SVC

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
		print(li)
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
				# arr[words.index(a1[1])] = 1
				# arr[tags.index(a1[4]) + len(words)] = 1
				# arr[chunk_tags.index(a1[3]) + len(words) + len(tags)] = 1

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
				# arr[words.index('ROOT')] = 1
				# arr[tags.index('ROOT') + len(words)] = 1
				# arr[chunk_tags.index('ROOT') + len(words) + len(tags)] = 1

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
			# arr[z + words.index(a2[2])] = 1
			# arr[z + tags.index(a2[5]) + len(words)] = 1
			# arr[z + chunk_tags.index(a2[4]) + len(words) + len(tags)] = 1

			# X.append(arr.astype(int))
			Y.append(a3[1])


X = csr_matrix((data, (row, column)))
clf = SVC()
clf.fit(X, Y)