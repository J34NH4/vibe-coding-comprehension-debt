from collections import defaultdict, deque

class Solution:
    def findMinHeightTrees(self, n, edges):
        if n == 1: return [0]
        g = defaultdict(set)
        for u, v in edges:
            g[u].add(v)
            g[v].add(u)
        q = deque([i for i in range(n) if len(g[i]) == 1])
        while n > 2:
            s = len(q)
            n -= s
            for _ in range(s):
                l = q.popleft()
                nb = g[l].pop()
                g[nb].remove(l)
                if len(g[nb]) == 1:
                    q.append(nb)
        return list(q)