class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2: return s
        st, mx = 0, 1
        for i in range(n):
            for j in range(2):
                l, r = i, i + j
                while l >= 0 and r < n and s[l] == s[r]:
                    if r - l + 1 > mx:
                        st, mx = l, r - l + 1
                    l -= 1
                    r += 1
        return s[st:st + mx]