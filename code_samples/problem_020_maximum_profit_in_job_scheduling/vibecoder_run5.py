class Solution:
    def jobScheduling(self, s, e, p):
        from bisect import bisect_left
        j = sorted(zip(e, s, p))
        dp = [0] * (len(j) + 1)
        for i in range(len(j)):
            k = bisect_left([x[0] for x in j[:i]], j[i][1])
            dp[i + 1] = max(dp[i], dp[k] + j[i][2])
        return dp[-1]