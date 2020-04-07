import sys
import re
import copy
from collections import deque


count=0
line_state=[]
line_id=[]
training_tags=[]
buffer=[]
dependency=[]
line_number=0
with open(sys.argv[1], 'r') as f:
	for line in f:
		line_number+=1 #for calculating the line to print .Currently used to print buffer
		pattern_start=re.compile("<S+")
		pattern_end=re.compile("</S+")
		pattern_head=re.compile("H+")
		if pattern_start.match(line):
			line_number=0
			count+=1 #Calculating sentence number
			line_id.append(count) #type_int 

		if pattern_head.match(line): #character matches head part
			line1=line.split(";")
			line2=line1[0].split()
			line_state.append(line_id[0])
			line_state.append(line2[5])
			line2=line1[1].split() #split into elements 
			if (len(line2)==1):
				line_state.append(line2[0]) #root word
			else:
				line_state.append(line2[5]) #extracting the unique head name
			
			line_state.append(line1[2][2])
			line2=line1[3].strip()
			line_state.append(line2)

			#print(line_state)
			temp_line_state=copy.copy(line_state) 
			training_tags.append(temp_line_state)
			line_state.clear()

		if pattern_end.match(line):
			line_id.pop()
		if line_number == 8:
			temp=[]
			temp.append(count)
			line=line.split()
			temp.append(line)
			#print(len(line))
			buffer.append(temp)

# def left_arc(stack,size):
# 	temp=[]
# 	stack_top=stack[size]
# 	for i in training_tags:
# 		if stack_top==i[1] and i[3]=="R":
# 			for j in training_tags:
# 				if stack_top==i[1] and i[3]=="R":
# 					flag=-1
# 					break
# 				else:



#print (buffer)
#print(training_tags)
#print(len(buffer))
for i in range(len(buffer)):
	line=copy.copy(buffer[i][1])
	#print(line)
	stack=deque()
	condition=0
	while condition==0:
		initialiser="ROOT"
		stack.append(initialiser)
		
