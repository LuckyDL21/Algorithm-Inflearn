# 6시 30분 ~ 6시 40분
# 최소 몇 대 카메라 설치 need? 

"""
[방법 01]

- deque로 prices를 하나씩 popleft 하면서, 그 값을 기준(standard)으로
  뒤에 남은 가격들과 하나씩 비교 (이중 루프: while + for)

- 비교 중 가격이 계속 standard 이상이면(안 떨어지면) ans += 1 하면서 계속 진행
  → 중간에 처음으로 standard보다 작은 값이 나오는 순간 "드롭 발생"으로 보고
     answer에 기록 후 break

- [주의 - 겪었던 버그]
  드롭이 발생한 그 순간(else 분기)은 ans가 증가하지 않고 멈춘 상태라서,
  ans를 그대로 쓰면 실제 경과 시간보다 항상 1 작게 나옴.
  → else 분기에서는 ans 대신 (idx + 1) 을 사용해야 정확한 초 단위가 나옴
     (idx+1 = 드롭이 확정된 시점까지의 실제 경과 시간)

- 드롭이 한 번도 없이 for문이 끝까지 도는 경우(all_done 분기)는
  매 스텝마다 ans가 계속 증가했으므로 ans == idx+1 이 자연히 성립 →
  이 경우엔 버그 없이 ans 그대로 써도 무방

- [시간복잡도]
  while(popleft) 안에 for(남은 원소 전체 비교)가 중첩된 구조라 O(n^2).
  n=100,000 기준으로는 TLE 위험 있음 → 이후 스택으로 O(n) 개선 여지 있음

[방법 02]

[방법 02]

- 스택(index_stack)에는 "아직 하락을 못 만난 인덱스들"만 쌓아둠.
  값 자체가 아니라 인덱스를 쌓는 게 포인트 (걸린 시간 = i - top 계산에 인덱스 필요)

- 배열을 처음부터 끝까지 딱 한 번만 순회(for i in range(n)):
  → 새 인덱스 i를 볼 때마다, 스택 top의 가격이 지금 가격보다 크면
     "top이 드디어 자기보다 낮은 값을 만났다"는 뜻이므로 pop하고
     answer[top] = i - top 로 확정
  → 스택 top이 더 이상 크지 않을 때까지 while로 반복 pop
  → 다 pop하고 나면 현재 인덱스 i를 스택에 push

- 순회가 다 끝난 뒤 스택에 남아있는 인덱스들은 끝까지 한 번도 안 떨어진 것
  → answer[top] = (n-1) - top 으로 마무리 처리 (별도 while로 전부 pop하며 채움)

- [주의 - 방법 01과 다른 점]
  answer를 append로 채우면 순서가 꼬이므로, 처음부터
  answer = [0] * n 으로 자리 확보해두고 answer[top] = ... 식으로
  "확정된 인덱스의 자리"에 직접 넣어야 함 (i 자리가 아니라 top 자리!)

- [시간복잡도 - 이중 루프처럼 보이지만 O(n)인 이유]
  for 안에 while이 있어 언뜻 O(n^2)처럼 보이지만,
  각 인덱스는 스택에 딱 한 번만 push되고 딱 한 번만 pop됨
  → 전체 push 총합 = n, pop 총합 ≤ n → while이 여러 번 도는 순간이 있어도
     다 더하면 절대 n을 못 넘음 (상각 분석, amortized O(1) per element)
  → 전체 시간복잡도 O(n)


"""

# 방법 01

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


# 방법 02

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