class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        d,l,m={},-1,0
        for i,c in enumerate(s):
            if c in d and d[c]>l:l=d[c]
            d[c]=i
            m=max(m,i-l)
        return m