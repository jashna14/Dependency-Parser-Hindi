import sys
import re
count = 0
w = 0
with open(sys.argv[1], 'r') as f:
    flag = 0 
    cnt = 0
    for line in f:
        if (line.rstrip()):
            if(line.strip() == '<text>'):
                flag = 1
                continue
            elif(line.strip() == '</text>'):
                flag = 0
                continue

            if(flag == 1):
                if(line.split(' ')[0] == '<Sentence'):
                    cnt += 1
                    print('<Sentence id=\'' + str(cnt) + '\'>')
                else:    
                    print(line.strip())        
