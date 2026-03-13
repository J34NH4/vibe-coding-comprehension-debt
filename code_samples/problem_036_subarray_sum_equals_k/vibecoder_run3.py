class Solution:
    def subarraySum(self, nums, k):
        c = {0: 1}
        s = r = 0
        for n in nums:
            s += n
            r += c.get(s - k, 0)
            c[s] = c.get(s, 0) + 1
        return r