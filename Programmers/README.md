# 프로그래머스 - 단속카메라 (Level 3)

문제: https://school.programmers.co.kr/learn/courses/30/lessons/42884

차량의 진입/진출 구간이 여러 개 주어질 때, 모든 차량을 단속하기 위한
**최소 카메라 개수**를 구하는 문제. 대표적인 구간 스케줄링 그리디 유형.

---

## 방법 1 — while + deque 재필터링 (첫 시도)

### 아이디어
- 진출 지점 기준 정렬 후, `while` 루프를 돌면서
  아직 커버되지 않은 route들만 걸러 새로운 deque로 다시 만드는 방식.
- 매 반복마다 "카메라 하나 설치 → 남은 것들 재필터링"을 반복.

### 코드
```python
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
```

### 문제점
- 정답은 맞지만 `while` 루프 안에서 매번 남은 리스트 전체를 `for`로
  다시 훑기 때문에 **최악의 경우 O(n²)**.
- routes 최대 100,000개 제약을 고려하면 시간 초과(TLE) 가능성 높음.

---

## 방법 2 — 단일 for 루프 그리디 (최종 정답)

### 아이디어
- 정렬을 한 번만 해두면, 왼쪽에서 오른쪽으로 **한 방향으로 한 번만 순회**
  하면서 그 자리에서 바로 커버 여부를 판단할 수 있음.
- 재필터링(새 리스트 생성) 자체가 불필요 — 정렬이 이미 순서를 보장해줌.
- 핵심 트릭: `last_camera`의 초기값을 `float('-inf')`로 잡아야
  첫 번째 route도 정상적으로 카메라 1대로 카운트됨.
  (`routes_sorted[0][1]`로 초기화하면 첫 카메라 설치가 answer에
  반영되지 않는 버그 발생)

### 코드
```python
def solution(routes):
    routes.sort(key=lambda x: x[1])  # 진출 지점 기준 정렬

    answer = 0
    last_camera = float('-inf')  # 아직 카메라 없음 상태로 초기화

    for start, end in routes:
        if start > last_camera:      # 기존 카메라로 커버 안 되는 차량
            answer += 1
            last_camera = end        # 새 카메라를 진출 지점에 설치

    return answer
```

### 왜 정답인가 (그리디 정당성)
- 진출 지점 기준 정렬 → 카메라를 항상 "가능한 한 뒤쪽"에 설치하게 됨
- 뒤쪽에 설치할수록 이후 겹치는 차량들을 더 많이 커버 가능
- "각 시점의 최선 선택이 전체 최적해로 이어진다"는 그리디 조건 만족
  (교환 논증으로 증명 가능)

---

## 비교

| | 방법 1 (while+deque) | 방법 2 (for 루프) |
|---|---|---|
| 정렬 | O(n log n) | O(n log n) |
| 본문 로직 | O(n²) (재필터링 반복) | O(n) (단일 순회) |
| 전체 시간복잡도 | **O(n²)** | **O(n log n)** |
| n=100,000일 때 | TLE 위험 | 안전 |

**결론**: 로직 자체(그리디 판단 기준)는 두 방법 모두 동일하게 맞았지만,
"커버 안 된 것들을 다시 걸러서 재검사"하는 구조 vs "정렬해두고 한 번만
순회"하는 구조의 차이가 시간복잡도를 O(n²)에서 O(n log n)으로 갈랐다.
