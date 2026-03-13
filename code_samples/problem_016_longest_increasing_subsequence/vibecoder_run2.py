class Solution:
    def lengthOfLIS(self, nums):
        dp = []
        for n in nums:
            l, r = 0, len(dp)
            while l < r:
                m = (l + r) // 2
                if dp[m] < n:
                    l = m + 1
                else:
                    r = m
            if l == len(dp):
                dp.append(n)
            else:
                dp[l] = n
        return len(dp)