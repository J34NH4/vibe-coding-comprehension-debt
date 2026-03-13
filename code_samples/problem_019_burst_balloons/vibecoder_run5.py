class Solution:
    def maxCoins(self, nums):
        n = [1] + [x for x in nums if x > 0] + [1]
        m = len(n)
        dp = [[0] * m for _ in range(m)]
        for l in range(2, m):
            for i in range(m - l):
                j = i + l
                for k in range(i + 1, j):
                    dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + n[i] * n[k] * n[j])
        return dp[0][m - 1]