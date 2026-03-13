class Solution:
    def findWords(self, board, words):
        class T:
            def __init__(self):
                self.c = {}
                self.w = False
        
        r = T()
        for w in words:
            n = r
            for c in w:
                if c not in n.c: n.c[c] = T()
                n = n.c[c]
            n.w = w
        
        m, n, res = len(board), len(board[0]), []
        
        def d(i, j, t):
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] not in t.c: return
            c, board[i][j] = board[i][j], '#'
            t = t.c[c]
            if t.w: res.append(t.w); t.w = False
            for x, y in [(0,1),(1,0),(0,-1),(-1,0)]: d(i+x, j+y, t)
            board[i][j] = c
        
        for i in range(m):
            for j in range(n): d(i, j, r)
        return res