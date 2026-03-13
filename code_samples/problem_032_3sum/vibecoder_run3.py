class Solution:
    def threeSum(self, nums):
        nums.sort()
        r = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            l, h = i + 1, len(nums) - 1
            while l < h:
                s = nums[i] + nums[l] + nums[h]
                if s < 0:
                    l += 1
                elif s > 0:
                    h -= 1
                else:
                    r.append([nums[i], nums[l], nums[h]])
                    while l < h and nums[l] == nums[l+1]:
                        l += 1
                    while l < h and nums[h] == nums[h-1]:
                        h -= 1
                    l += 1
                    h -= 1
        return r