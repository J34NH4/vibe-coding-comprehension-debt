from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t: return ""
        tc = Counter(t)
        wc = {}
        l, r = 0, 0
        req = len(tc)
        formed = 0
        ans = float("inf"), None, None
        while r < len(s):
            c = s[r]
            wc[c] = wc.get(c, 0) + 1
            if c in tc and wc[c] == tc[c]:
                formed += 1
            while l <= r and formed == req:
                c = s[l]
                if r - l + 1 < ans[0]:
                    ans = (r - l + 1, l, r)
                wc[c] -= 1
                if c in tc and wc[c] < tc[c]:
                    formed -= 1
                l += 1    
            r += 1    
        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]