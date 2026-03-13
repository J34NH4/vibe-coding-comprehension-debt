class Solution:
    def lengthOfLongestSubstring(self, s):
        n = len(s)
        if n <= 1: return n
        m = 0
        for i in range(n):
            c = set()
            for j in range(i, n):
                if s[j] in c: break
                c.add(s[j])
                m = max(m, j - i + 1)
        return m