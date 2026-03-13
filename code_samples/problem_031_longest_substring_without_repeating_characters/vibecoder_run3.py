class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        m,l,r=0,0,0
        c=set()
        while r<len(s):
            while s[r] in c:
                c.remove(s[l])
                l+=1
            c.add(s[r])
            m=max(m,r-l+1)
            r+=1
        return m