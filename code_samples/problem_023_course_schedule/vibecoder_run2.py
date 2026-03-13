from collections import defaultdict, deque

class Solution:
    def canFinish(self, n, p):
        g = defaultdict(list)
        d = [0] * n
        for a, b in p:
            g[b].append(a)
            d[a] += 1
        q = deque([i for i in range(n) if d[i] == 0])
        c = 0
        while q:
            x = q.popleft()
            c += 1
            for y in g[x]:
                d[y] -= 1
                if d[y] == 0:
                    q.append(y)
        return c == n