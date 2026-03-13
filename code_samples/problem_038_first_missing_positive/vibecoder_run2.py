class Solution:
    def firstMissingPositive(self, nums):
        n = len(nums)
        for i in range(n):
            if nums[i] <= 0 or nums[i] > n:
                nums[i] = n + 1
        for i in range(n):
            x = abs(nums[i])
            if x <= n:
                nums[x - 1] = -abs(nums[x - 1])
        for i in range(n):
            if nums[i] > 0:
                return i + 1
        return n + 1