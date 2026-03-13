class Solution:
    def permute(self, nums):
        if not nums: return [[]]
        r = []
        for i, x in enumerate(nums):
            for p in self.permute(nums[:i] + nums[i+1:]):
                r.append([x] + p)
        return r