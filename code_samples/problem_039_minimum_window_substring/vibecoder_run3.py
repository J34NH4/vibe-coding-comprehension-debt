from collections import Counter, defaultdict

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t: return ""
        d = Counter(t)
        r = len(d)
        l = ri = 0
        w = defaultdict(int)
        a = float("inf"), None, None
        for ri in range(len(s)):
            c = s[ri]
            w[c] += 1
            if c in d and w[c] == d[c]:
                r -= 1
            while l <= ri and r == 0:
                c = s[l]
                if a[0] > ri - l + 1:
                    a = ri - l + 1, l, ri
                w[c] -= 1
                if c in d and w[c] < d[c]:
                    r += 1
                l += 1
        return "" if a[0] == float("inf") else s[a[1]:a[2]+1]