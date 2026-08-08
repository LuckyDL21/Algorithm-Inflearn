"""
프로그래머스 Level 3 - 단속카메라
https://school.programmers.co.kr/learn/courses/30/lessons/42884

[문제 요약]
차량이 고속도로를 통과하는 구간 [진입, 진출] 정보가 여러 개 주어질 때,
모든 차량을 단속하기 위해 필요한 최소 카메라 개수를 구하시오.

[입출력 예]
routes = [[-20,-15], [-14,-5], [-18,-13], [-5,-3]]
-> 정답: 2

[힌트 - 필요할 때만 하나씩 열어볼 것]

힌트 1)
    전형적인 "구간 스케줄링" 계열 그리디 문제야.
    정렬 기준을 뭘로 잡을지가 핵심.

힌트 2)
    진입 지점(routes[i][0])이 아니라
    ○○ 지점(routes[i][1]) 기준으로 정렬해봐.
    왜 그게 유리한지 생각해볼 것.

힌트 3)
    정렬 후 순회하면서, 마지막으로 설치한 카메라 위치를 변수로 들고 있다가
    현재 차량의 진입 지점이 그 위치보다 "뒤"에 있으면 커버가 안 된 거니까
    새 카메라를 설치해야 함. 이때 카메라는 어디에 설치하는 게 최선일까?
    (진출 지점 vs 진입 지점 — 뒤쪽에 설치할수록 이후 차량도 더 많이 커버 가능)

[시간복잡도 목표] O(n log n)
"""


def solution(routes):
    # TODO: 여기에 직접 구현
    pass


if __name__ == "__main__":
    test_cases = [
        ([[-20, -15], [-14, -5], [-18, -13], [-5, -3]], 2),
    ]

    for routes, expected in test_cases:
        result = solution(routes)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] routes={routes} -> result={result} (expected={expected})")
