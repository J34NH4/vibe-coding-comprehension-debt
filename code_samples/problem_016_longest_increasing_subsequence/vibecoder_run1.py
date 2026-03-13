from bisect import bisect_left

class Solution:
    def lengthOfLIS(self, nums):
        t = []
        for n in nums:
            i = bisect_left(t, n)
            if i == len(t): t.append(n)
            else: t[i] = n
        return len(t)