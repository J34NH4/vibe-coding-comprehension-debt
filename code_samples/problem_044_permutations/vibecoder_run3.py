class Solution:
    def permute(self, nums):
        if not nums: return [[]]
        r = []
        for i in range(len(nums)):
            for p in self.permute(nums[:i] + nums[i+1:]):
                r.append([nums[i]] + p)
        return r