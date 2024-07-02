# Greedy Algorithm
import sys

"""
5
172 67
183 65
180 70
170 72
181 60
"""
n=int(input())

h_w_info=[]

for i in range(n):
    h,w=map(int,input().split())
    h_w_info.append((h,w))

minus=0
h_w_info.sort(key=lambda x: (x[1],x[0]))

for i in range(len(h_w_info)-1):
    
    sub_count=0
    h,w = h_w_info[i]

    for j in range(i+1,len(h_w_info)):
        h_,w_ = h_w_info[j]
        if h<=h_ and w<=w_:
            minus+=1
            break

answer=n-minus
print(answer)