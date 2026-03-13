from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t or len(s) < len(t): return ""
        tc = Counter(t)
        l = r = 0
        mn = float('inf')
        res = ""
        need = len(tc)
        have = 0
        wc = {}
        while r < len(s):
            c = s[r]
            wc[c] = wc.get(c, 0) + 1
            if c in tc and wc[c] == tc[c]: have += 1
            while have == need:
                if r - l + 1 < mn:
                    mn = r - l + 1
                    res = s[l:r+1]
                lc = s[l]
                wc[lc] -= 1
                if lc in tc and wc[lc] < tc[lc]: have -= 1
                l += 1
            r += 1
        return res