class Solution:
    def exist(self, board, word):
        m, n, w = len(board), len(board[0]), len(word)
        def dfs(i, j, k):
            if k == w: return True
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]: return False
            t = board[i][j]
            board[i][j] = '#'
            r = any(dfs(i+x, j+y, k+1) for x, y in [(0,1),(0,-1),(1,0),(-1,0)])
            board[i][j] = t
            return r
        return any(dfs(i, j, 0) for i in range(m) for j in range(n))