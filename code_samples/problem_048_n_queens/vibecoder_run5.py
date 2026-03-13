class Solution:
    def solveNQueens(self, n):
        r = []
        def b(c, p, d1, d2):
            if c == n:
                r.append(['.' * i + 'Q' + '.' * (n - i - 1) for i in p])
                return
            for i in range(n):
                if i not in p and c - i not in d1 and c + i not in d2:
                    b(c + 1, p + [i], d1 | {c - i}, d2 | {c + i})
        b(0, [], set(), set())
        return r