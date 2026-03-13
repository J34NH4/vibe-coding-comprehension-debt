class Solution:
    def subarraySum(self, nums, k):
        c = 0
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                if s == k:
                    c += 1
        return c