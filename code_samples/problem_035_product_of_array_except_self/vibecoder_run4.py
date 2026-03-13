class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        res = [1] * n
        for i in range(1, n):
            res[i] = res[i-1] * nums[i-1]
        r = 1
        for i in range(n-1, -1, -1):
            res[i] *= r
            r *= nums[i]
        return res