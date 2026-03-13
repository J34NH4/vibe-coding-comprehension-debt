class Solution:
    def solveNQueens(self, n):
        r = []
        def b(q, c, d1, d2):
            if len(q) == n:
                r.append(['.' * i + 'Q' + '.' * (n - i - 1) for i in q])
                return
            for i in range(n):
                if i not in c and len(q) - i not in d1 and len(q) + i not in d2:
                    b(q + [i], c | {i}, d1 | {len(q) - i}, d2 | {len(q) + i})
        b([], set(), set(), set())
        return r