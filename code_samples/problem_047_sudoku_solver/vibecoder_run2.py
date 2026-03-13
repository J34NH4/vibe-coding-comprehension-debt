class Solution:
    def solveSudoku(self, b):
        def v(r, c, n):
            return n not in b[r] and n not in [b[i][c] for i in range(9)] and n not in [b[r//3*3+i//3][c//3*3+i%3] for i in range(9)]
        def s():
            for r in range(9):
                for c in range(9):
                    if b[r][c] == '.':
                        for n in '123456789':
                            if v(r, c, n):
                                b[r][c] = n
                                if s(): return True
                                b[r][c] = '.'
                        return False
            return True
        s()