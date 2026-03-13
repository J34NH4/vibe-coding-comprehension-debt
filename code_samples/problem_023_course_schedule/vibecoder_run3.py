class Solution:
    def canFinish(self, n: int, p: List[List[int]]) -> bool:
        g = [[] for _ in range(n)]
        d = [0] * n
        for a, b in p:
            g[b].append(a)
            d[a] += 1
        q = [i for i in range(n) if d[i] == 0]
        c = 0
        while q:
            x = q.pop(0)
            c += 1
            for y in g[x]:
                d[y] -= 1
                if d[y] == 0:
                    q.append(y)
        return c == n