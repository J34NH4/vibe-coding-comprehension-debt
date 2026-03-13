class Solution:
    def lengthOfLIS(self, nums):
        from bisect import bisect_left
        dp = []
        for n in nums:
            i = bisect_left(dp, n)
            if i == len(dp): dp.append(n)
            else: dp[i] = n
        return len(dp)