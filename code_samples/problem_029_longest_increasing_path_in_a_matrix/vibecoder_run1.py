class Solution:
    def longestIncreasingPath(self, m):
        if not m or not m[0]: return 0
        r, c = len(m), len(m[0])
        dp = {}
        def dfs(i, j):
            if (i, j) in dp: return dp[(i, j)]
            res = 1
            for di, dj in [(0,1),(1,0),(0,-1),(-1,0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < r and 0 <= nj < c and m[ni][nj] > m[i][j]:
                    res = max(res, 1 + dfs(ni, nj))
            dp[(i, j)] = res
            return res
        return max(dfs(i, j) for i in range(r) for j in range(c))