class Solution:
    def solveNQueens(self, n):
        def b(r, c, d1, d2):
            if r == n: return [[]]
            s = []
            for i in range(n):
                if i not in c and r-i not in d1 and r+i not in d2:
                    for x in b(r+1, c|{i}, d1|{r-i}, d2|{r+i}):
                        s.append([i] + x)
            return s
        return [['.' * i + 'Q' + '.' * (n-1-i) for i in p] for p in b(0, set(), set(), set())]