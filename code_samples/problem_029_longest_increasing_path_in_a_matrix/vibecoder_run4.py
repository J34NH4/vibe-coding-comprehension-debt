class Solution:
    def longestIncreasingPath(self, matrix):
        if not matrix: return 0
        m, n = len(matrix), len(matrix[0])
        dp = {}
        
        def dfs(i, j):
            if (i, j) in dp: return dp[(i, j)]
            res = 1
            for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                    res = max(res, 1 + dfs(ni, nj))
            dp[(i, j)] = res
            return res
        
        return max(dfs(i, j) for i in range(m) for j in range(n))