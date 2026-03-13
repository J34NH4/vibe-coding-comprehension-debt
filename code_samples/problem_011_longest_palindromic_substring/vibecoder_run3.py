class Solution:
    def longestPalindrome(self, s):
        n = len(s)
        if n < 2: return s
        r = ""
        for i in range(n):
            for j in range(i, n):
                t = s[i:j+1]
                if t == t[::-1] and len(t) > len(r):
                    r = t
        return r