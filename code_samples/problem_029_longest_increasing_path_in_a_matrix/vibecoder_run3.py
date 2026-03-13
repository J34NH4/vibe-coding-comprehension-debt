class Solution:
    def longestIncreasingPath(self, matrix):
        m, n = len(matrix), len(matrix[0])
        c = {}
        def d(i, j):
            if (i, j) in c: return c[(i, j)]
            c[(i, j)] = 1 + max([d(x, y) for x, y in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)] if 0<=x<m and 0<=y<n and matrix[x][y]>matrix[i][j]] or [0])
            return c[(i, j)]
        return max(d(i, j) for i in range(m) for j in range(n))