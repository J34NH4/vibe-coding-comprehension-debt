class Solution:
    def subsets(self, nums):
        r = []
        for i in range(2**len(nums)):
            s = []
            for j in range(len(nums)):
                if i & (1 << j):
                    s.append(nums[j])
            r.append(s)
        return r