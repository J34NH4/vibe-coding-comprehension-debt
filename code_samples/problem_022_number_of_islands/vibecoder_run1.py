class Solution:
    def numIslands(self, grid):
        if not grid: return 0
        m, n, c = len(grid), len(grid[0]), 0
        def dfs(i, j):
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1': return
            grid[i][j] = '0'
            [dfs(i+di, j+dj) for di, dj in [(0,1),(1,0),(0,-1),(-1,0)]]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1': dfs(i, j); c += 1
        return c