class Solution:
    def wordBreak(self, s, wordDict):
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        w = set(wordDict)
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in w:
                    dp[i] = True
                    break
        return dp[n]