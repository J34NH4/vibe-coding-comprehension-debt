class Solution:
    def longestIncreasingPath(self, m):
        if not m or not m[0]: return 0
        r, c = len(m), len(m[0])
        dp = {}
        def dfs(i, j):
            if (i, j) in dp: return dp[(i, j)]
            res = 1
            for x, y in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]:
                if 0 <= x < r and 0 <= y < c and m[x][y] > m[i][j]:
                    res = max(res, 1 + dfs(x, y))
            dp[(i, j)] = res
            return res
        return max(dfs(i, j) for i in range(r) for j in range(c))