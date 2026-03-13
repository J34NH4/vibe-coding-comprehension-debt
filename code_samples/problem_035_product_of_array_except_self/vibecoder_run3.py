class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        r = [1] * n
        for i in range(1, n):
            r[i] = r[i-1] * nums[i-1]
        p = 1
        for i in range(n-1, -1, -1):
            r[i] *= p
            p *= nums[i]
        return r