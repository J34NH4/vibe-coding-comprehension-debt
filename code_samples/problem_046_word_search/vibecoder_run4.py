class Solution:
    def exist(self, board, word):
        m, n, w = len(board), len(board[0]), len(word)
        def dfs(i, j, k):
            if k == w: return True
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]: return False
            c = board[i][j]
            board[i][j] = '#'
            r = dfs(i+1,j,k+1) or dfs(i-1,j,k+1) or dfs(i,j+1,k+1) or dfs(i,j-1,k+1)
            board[i][j] = c
            return r
        return any(dfs(i,j,0) for i in range(m) for j in range(n))