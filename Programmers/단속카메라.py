# 6시 30분 ~ 6시 40분
# 최소 몇 대 카메라 설치 need? 

"""
* 생각: 첫번째 요소는 최대, 두번째 요소에는 최소 넣어서 하나씩 증가 , 증감 해서 가장 적은 route 출력ㅇ이
답이 아닐까 - 부분 집합으로 접근하는 방식을 말하나 이렇게 하면 답도 없다. 
-- 라이브러리 : from itertools import combinations,chain

"""

# 방법 01

from collections import deque

def solution(routes):
    routes_sorted = deque(sorted(routes, key=lambda x: x[1]))
    answer = 0

    while routes_sorted:
        answer += 1
        _, camera = routes_sorted.popleft()

        remaining = deque()
        for value in routes_sorted:
            if value[0] > camera:
                remaining.append(value)  # 아직 커버 안 된 것만 남김
        routes_sorted = remaining

    return answer


# 방법 02

def solution(routes):

    #answer=0
    
    routes_sorted = deque(sorted(routes,key=lambda x:x[1]))

    #print(routes_sorted)
    
    answer=0
    last_camera= float('-inf')
    
    for start,end in routes_sorted:
        if start>last_camera:
            answer+=1
            last_camera=end
                
    return answer