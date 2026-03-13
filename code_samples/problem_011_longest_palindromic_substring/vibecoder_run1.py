class Solution:
    def longestPalindrome(self, s):
        n = len(s)
        if n < 2: return s
        st, mx = 0, 1
        for i in range(n):
            l, r = i, i
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l + 1 > mx:
                    st, mx = l, r - l + 1
                l -= 1
                r += 1
            l, r = i, i + 1
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l + 1 > mx:
                    st, mx = l, r - l + 1
                l -= 1
                r += 1
        return s[st:st + mx]