from collections import deque

class Solution:
    def orangesRotting(self, grid):
        m, n = len(grid), len(grid[0])
        q = deque()
        f = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j, 0))
                elif grid[i][j] == 1:
                    f += 1
        if f == 0:
            return 0
        d = [(0,1),(0,-1),(1,0),(-1,0)]
        t = 0
        while q:
            x, y, t = q.popleft()
            for dx, dy in d:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                    grid[nx][ny] = 2
                    f -= 1
                    q.append((nx, ny, t + 1))
        return t if f == 0 else -1