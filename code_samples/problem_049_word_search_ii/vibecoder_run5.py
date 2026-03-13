class Solution:
    def findWords(self, board, words):
        class T:
            def __init__(self):
                self.c = {}
                self.w = None
        
        r = T()
        for w in words:
            n = r
            for c in w:
                if c not in n.c: n.c[c] = T()
                n = n.c[c]
            n.w = w
        
        m, n, res = len(board), len(board[0]), []
        
        def dfs(i, j, t):
            c = board[i][j]
            if c not in t.c: return
            t = t.c[c]
            if t.w:
                res.append(t.w)
                t.w = None
            board[i][j] = '#'
            for di, dj in [(0,1),(1,0),(0,-1),(-1,0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, t)
            board[i][j] = c
        
        for i in range(m):
            for j in range(n):
                dfs(i, j, r)
        return res