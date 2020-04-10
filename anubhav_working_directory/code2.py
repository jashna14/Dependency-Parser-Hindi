import sys
import re
import copy
from collections import deque

buffer=[]
line_state=[]
tags=[]
dependencies=[]
line_number=0
def leftarc(node1,node2,stack,reln):
    if len(stack)==0:
        return -1
    else:
        tempo=[]
        tempo.append(node1)
        tempo.append(node2)
        tempo.append("l")
        tempo.append(reln)
        temp1=copy.copy(tempo)
        dependencies.append(temp1)
        stack.pop()
        return stack
def rightarc(node1,node2,stack,reln):
    if len(buffer)==0:
        return -1
    else:
        tempo=[]
        tempo.append(node1)
        tempo.append(node2)
        tempo.append("r")
        tempo.append(reln)
        temp1=copy.copy(tempo)
        dependencies.append(temp1)
        top_element=buffer.pop()
        stack.append(top_element)
        return stack
def reduction(stack):
    if len(stack)==0:
        return -1
    else:
        stack.pop()
        return stack
def shift (stack):
    if len(buffer)==0:
        return -1
    else :
        buff_top=buffer.pop()
        stack.append(buff_top)
        return stack



def predict (stack):
    flag=0
    stack_top=-1
    if len(stack)>0:
        stack_top=stack[len(stack)-1]

    buff_top=-1
    if len(buffer)>0:
        length=len(buffer)
        buff_top=buffer[length-1]
    
    #print(buffer)
    for i in tags:
        if stack_top!=-1 and stack_top==i[0]:
            if buff_top==i[1] and i[2]=='R':
                flag_left=0
                for j in tags:
                    if stack_top==j[0] and j[2]=='R':
                        if i==j:
                            continue
                        else :
                            flag_left=1
                            break
                if flag_left==0:
                    flag=1
                    #print(flag)
                    stack=leftarc(i[0],i[1],stack,i[3])
                    return flag,stack

        if buff_top!=-1 and stack_top==i[0]:
            if buff_top==i[1] and i[2]=='L':
                flag_right=0
                for j in tags:
                    if buff_top==j[0] and j[2]=='L':
                        if i==j:
                            continue
                        else:
                            flag_right=1
                            break
                if flag_right==0:
                    flag=2
                   # print(flag)
                    stack=rightarc(i[0],i[1],stack,i[3])
                    return flag,stack

        if buff_top!=-1:
            flag=3
            #print(flag)
            stack=shift(stack)
            return flag,stack

        if stack_top!=-1:
            flag_reduce=0
            for j in tags:
                if stack_top==j[0] and j[3]=='R':
                    flag_reduce=1
                    break
                if stack_top==j[1] and j[3]=='L':
                    flag_reduce=1
                    break
            if flag_reduce==1:
                stack=reduction(stack)
                flag=4
                #print(flag)
                return flag,stack
        if flag==0:
            #print(flag)
            flag=5
            return flag,stack


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
            
            condition=0
            flag=0
            while condition<12:
                flag,stack= predict(stack)
                #print(flag)
                #print(stack)
                condition+=1                

            #print(buffer)
            #print(tags)
            #print(dependencies)
            tags.clear()

        if line_number == 8:
            buffer.clear()
            line=line.split()
            for i in line:   
                buffer.append(i)
            buffer.reverse()
            
