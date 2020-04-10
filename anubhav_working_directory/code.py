import sys
import re
import copy
from collections import deque


count=0
line_state=[]
line_id=[]
buffer=[]
training_tags=[]
dependency=[]
line_number=0
def checker(buffer,local_dependency,idx,hold,stack_top):
	flag=0
	for j in range(len(local_dependency)):
		if buffer[1][idx]==local_dependency[j][2] and local_dependency[j][3]=="R":
			if stack_top==local_dependency[j][1]:
				if j!=hold:
					flag=1
					break
	if flag==0:
		return 1
	else:
		return 0
	

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
			local_dependency=[]
			#print(len(line))
			stack=deque()
			initialiser="ROOT"
			stack.append(initialiser)
			for j in training_tags:
				if buffer[0]==j[0]:
					local_dependency.append(j)
			condition=0
			pointer_buffer=0
			print(stack)
			while condition==0:
				hold=0
				stack_top=stack[len(stack)-1]
				for j in range(len(local_dependency)):
					if buffer[1][pointer_buffer]==local_dependency[j][2] and local_dependency[j][3]=="R":
						if stack_top==local_dependency[j][1]:
							hold=j
							k=checker(buffer,local_dependency,pointer_buffer,hold,stack_top)
							if k==1:
								temp=[]
								temp.append(buffer[0])
								temp.append(buffer[1][pointer_buffer])
								temp.append(local_dependency[j][2])
								temp.append("l")
								temp2=copy.copy(temp)
								print(temp2)
								stack.pop()
								break
				for j in range(len(local_dependency)):
					


			# print(buffer)
			# print(local_dependency)
			line_id.pop()
		if line_number == 8:
			buffer.clear()
			buffer.append(count)
			line=line.split()
			buffer.append(line)
			
					



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


<<<<<<< HEAD

print (buffer)
print(training_tags)
#print(len(buffer))
for i in range(len(buffer)):
	line=copy.copy(buffer[i][1])
	#print(line)
	stack=deque()
	condition=0
	while condition==0:
		initialiser="ROOT"
		stack.append(initialiser)
		break
		
=======
>>>>>>> 2a7e362117502a50df94fafd6f0b10e3659e00af
