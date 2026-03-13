from collections import Counter
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t: return ""
        d = Counter(t)
        r = len(d)
        l = x = 0
        mn = float("inf")
        res = ""
        w = {}
        for i in range(len(s)):
            c = s[i]
            w[c] = w.get(c, 0) + 1
            if c in d and w[c] == d[c]:
                x += 1
            while l <= i and x == r:
                if i - l + 1 < mn:
                    mn = i - l + 1
                    res = s[l:i+1]
                ch = s[l]
                w[ch] -= 1
                if ch in d and w[ch] < d[ch]:
                    x -= 1
                l += 1
        return res