class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n, l, r, m, d = len(s), 0, 0, 0, {}
        while r < n:
            if s[r] in d and d[s[r]] >= l:
                l = d[s[r]] + 1
            d[s[r]] = r
            m = max(m, r - l + 1)
            r += 1
        return m