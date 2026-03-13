class Solution:
    def wordBreak(self, s, wordDict):
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        w = set(wordDict)
        for i in range(1, n + 1):
            dp[i] = any(dp[j] and s[j:i] in w for j in range(i))
        return dp[n]