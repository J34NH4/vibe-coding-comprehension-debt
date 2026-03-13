class Solution:
    def solveNQueens(self, n):
        def b(r, c, d1, d2):
            if r == n:
                return [['.' * i + 'Q' + '.' * (n - i - 1) for i in c]]
            return [s for i in range(n) if i not in c and r - i not in d1 and r + i not in d2 for s in b(r + 1, c + [i], d1 | {r - i}, d2 | {r + i})]
        return b(0, [], set(), set())