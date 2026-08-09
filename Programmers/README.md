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

---
---

# 프로그래머스 - 주식가격 (Level 2)

문제: https://school.programmers.co.kr/learn/courses/30/lessons/42584

가격이 순서대로 담긴 배열이 주어질 때, 각 가격이 "떨어지기 전까지 몇 초
동안 안 떨어졌는지"를 구하는 문제. 대표적인 **모노토닉 스택(monotonic
stack)** 유형 — "다음으로 더 작은 원소를 찾는" 패턴.

---

## 방법 1 — 이중 for 루프 (while + for, 첫 시도)

### 아이디어
- `deque`로 하나씩 popleft 하면서, 그 값을 기준(standard)으로 뒤에
  남은 가격들과 하나씩 비교하는 이중 루프(`while` 안에 `for`).
- 비교 중 가격이 계속 기준 이상이면 카운트(`ans`)만 늘리다가, 처음으로
  기준보다 작은 값이 나오는 순간 "드롭 발생"으로 보고 기록 후 break.

### 코드
```python
from collections import deque

def solution(prices):
    answer = []
    prices = deque(prices)

    while prices:
        ans = 0
        standard = prices.popleft()

        for idx, price in enumerate(prices):
            all_done = False
            if standard <= price:
                ans += 1
            else:
                answer.append(idx + 1)   # 드롭 확정 시점의 실제 경과 시간
                all_done = True
                break
            if idx == len(prices) - 1 and not all_done:
                answer.append(ans)

    answer.append(0)
    return answer
```

### 겪었던 버그
- 드롭이 발생한 순간(else 분기)에서 `ans`를 그대로 쓰면, 드롭이 확정된
  마지막 스텝 자체가 `ans` 카운팅에서 빠져 있어서 **항상 실제 경과 시간보다
  1 작게** 나옴 → `idx + 1`로 고쳐야 함.
- 반면 드롭이 한 번도 없이 for문이 끝까지 도는 경우(`all_done` 분기)는
  매 스텝 `ans`가 증가했으므로 `ans == idx+1`이 자연히 성립해서 버그 없음.

### 문제점
- `while`(popleft) 안에 `for`(남은 원소 전체 비교)가 중첩된 구조라
  **최악의 경우 O(n²)**.
- prices 최대 100,000개 제약 고려 시 TLE 위험.

---

## 방법 2 — 모노토닉 스택 (최종 정답, O(n))

### 아이디어
- 스택엔 "아직 하락을 못 만난 인덱스들"을 쌓아둠.
- 배열을 처음부터 끝까지 **한 번만** 순회하면서, 새 인덱스 `i`를 볼 때마다
  스택 top의 가격이 지금 가격보다 크면 → top이 드디어 자기보다 낮은 값을
  만난 것이므로 pop하고 `answer[top] = i - top` 확정.
- 순회가 끝나고 스택에 남은 인덱스들은 끝까지 안 떨어진 것이므로
  `answer[top] = (n-1) - top`으로 마무리.

### 코드
```python
def solution(prices):
    n = len(prices)
    answer = [0] * n
    index_stack = []

    for i in range(n):
        while index_stack and prices[index_stack[-1]] > prices[i]:
            top = index_stack.pop()
            answer[top] = i - top
        index_stack.append(i)

    while index_stack:
        top = index_stack.pop()
        answer[top] = (n - 1) - top

    return answer
```

### 왜 O(n)인가 (상각 분석)
- 겉보기엔 `for` 안에 `while`이 있어 이중 루프처럼 보이지만, **각 인덱스는
  스택에 딱 한 번만 push되고 딱 한 번만 pop됨**.
- 전체 실행 동안 push 총 횟수 = n, pop 총 횟수 ≤ n → `while`이 여러 번
  도는 순간이 있어도 다 더하면 절대 n을 못 넘음 → 전체 O(n).

---

## 비교

| | 방법 1 (이중 for) | 방법 2 (모노토닉 스택) |
|---|---|---|
| 본문 로직 | O(n²) | O(n) |
| n=100,000일 때 | TLE 위험 | 안전 |

**결론**: "각 원소가 최대 몇 번 push/pop되는지" 세어보는 상각 분석 감각이
이중 루프처럼 보이는 코드의 실제 시간복잡도를 판단하는 핵심이었다.
단속카메라와 마찬가지로, 로직의 정답 여부와 시간복잡도는 별개의 문제라는
걸 다시 확인.
