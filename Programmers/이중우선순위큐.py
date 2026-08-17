# 소요시간 : 22분

# 내 풀이 방법: 정확도가 100점이지만 시간복잡도 부분에서 n*n 이 걸린다는 단점이 존재합니다.
def solution(operations):
    
    element_list=[]
    
    for strings in operations:
        alpha,num = strings.split(" ")
        if alpha =="I":
            element_list.append(int(num))
        elif alpha=="D" and num=="1" and len(element_list)!=0:
            element_list.remove(max(element_list))
        elif alpha=="D" and num=="-1"and len(element_list)!=0:
            element_list.remove(min(element_list))
            
    if len(element_list)==0:
        return [0,0]
    else:
        return [max(element_list),min(element_list)]

# 두번째 접근 : heapq 이중으로 써서 탐색의 시간 복잡도를 줄일 수 있다.

import heapq

def solution(operations):
    
    answer = []
    
    min_heapq=[]
    max_heapq=[]
    
    delete_set = set()
    
    for idx,values in enumerate(operations):
        
        alpha,num=values.split(" ")
        num=int(num)
        
        if alpha=="I":
            heapq.heappush(min_heapq,(num,idx))
            heapq.heappush(max_heapq,(-num,idx))
        elif alpha=="D" and num==1:
            while max_heapq and max_heapq[0][1] in delete_set:
                heapq.heappop(max_heapq)
            if max_heapq:
                _,id=heapq.heappop(max_heapq)
                delete_set.add(id)
        elif alpha=="D" and num==-1:
            while min_heapq and min_heapq[0][1] in delete_set:
                heapq.heappop(min_heapq)
            if min_heapq:
                _,id=heapq.heappop(min_heapq)
                delete_set.add(id)
                
    while max_heapq and max_heapq[0][1] in delete_set:
        heapq.heappop(max_heapq)
    while min_heapq and min_heapq[0][1] in delete_set:
        heapq.heappop(min_heapq)
        
    if not max_heapq or not min_heapq:
        return [0,0]
    
    max_value,_ = heapq.heappop(max_heapq)
    min_value,_ = heapq.heappop(min_heapq)
    
    return [-max_value,min_value]
                
                
    #return answer