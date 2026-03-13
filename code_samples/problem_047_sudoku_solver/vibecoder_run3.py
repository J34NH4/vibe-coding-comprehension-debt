from typing import List

class Solution:
    def solveSudoku(self, b: List[List[str]]) -> None:
        def v(r, c, n):
            for i in range(9):
                if b[r][i] == n or b[i][c] == n: return False
            sr, sc = 3 * (r // 3), 3 * (c // 3)
            for i in range(sr, sr + 3):
                for j in range(sc, sc + 3):
                    if b[i][j] == n: return False
            return True
        
        def s():
            for i in range(9):
                for j in range(9):
                    if b[i][j] == '.':
                        for n in '123456789':
                            if v(i, j, n):
                                b[i][j] = n
                                if s(): return True
                                b[i][j] = '.'
                        return False
            return True
        
        s()