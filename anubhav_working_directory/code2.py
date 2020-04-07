import sys
import re
import copy
from collections import deque

buffer=[]
line_state=[]
tags=[]
line_number=0

def predict (stack):
    pass
with open(sys.argv[1], 'r') as f:
    for line in f:
        line_number+=1
        pattern_start=re.compile("<S+")
        pattern_end=re.compile("</S+")
        pattern_head=re.compile("H+")

        if pattern_start.match(line):
            line_number=0
            
        if pattern_head.match(line): #character matches head part
            line1=line.split(";")
            line2=line1[0].split()
            line_state.append(line2[5])
            line2=line1[1].split() #split into elements 
            if (len(line2)==1):
                line_state.append(line2[0]) #root word
            else:
                line_state.append(line2[5]) #extracting the unique head name
            
            line_state.append(line1[2][2])
            line2=line1[3].strip()
            line_state.append(line2)
            temp_line_state=copy.copy(line_state) 
            tags.append(temp_line_state)
            line_state.clear()
        

        if pattern_end.match(line):
            stack=deque()
            initialiser="ROOT"
            stack.append(initialiser)
            #print(buffer)
            #print(stack)
            #print(tags)
            #initialised stack , buffer and have dependencies
            tags.clear()

        if line_number == 8:
            buffer.clear()
            line=line.split()
            buffer.append(line)
