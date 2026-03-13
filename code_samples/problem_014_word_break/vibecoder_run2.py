class Solution:
    def wordBreak(self, s, w):
        n = len(s)
        d = [False] * (n + 1)
        d[0] = True
        for i in range(1, n + 1):
            d[i] = any(d[j] and s[j:i] in w for j in range(i))
        return d[n]