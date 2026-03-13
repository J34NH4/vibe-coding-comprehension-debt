class Solution:
    def jobScheduling(self, s, e, p):
        j = sorted(zip(s, e, p), key=lambda x: x[1])
        dp = [0] * len(j)
        dp[0] = j[0][2]
        for i in range(1, len(j)):
            k = -1
            for l in range(i-1, -1, -1):
                if j[l][1] <= j[i][0]:
                    k = l
                    break
            dp[i] = max(dp[i-1], j[i][2] + (dp[k] if k != -1 else 0))
        return dp[-1] if j else 0