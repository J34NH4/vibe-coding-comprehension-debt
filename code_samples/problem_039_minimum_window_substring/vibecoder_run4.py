from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t: return ""
        tc = Counter(t)
        wc = {}
        l = r = 0
        f = 0
        res = ""
        ml = float('inf')
        while r < len(s):
            c = s[r]
            wc[c] = wc.get(c, 0) + 1
            if c in tc and wc[c] == tc[c]:
                f += 1
            while l <= r and f == len(tc):
                if r - l + 1 < ml:
                    ml = r - l + 1
                    res = s[l:r+1]
                lc = s[l]
                wc[lc] -= 1
                if lc in tc and wc[lc] < tc[lc]:
                    f -= 1
                l += 1
            r += 1
        return res