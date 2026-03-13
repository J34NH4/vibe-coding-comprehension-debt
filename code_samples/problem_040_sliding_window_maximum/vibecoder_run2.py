from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        d = deque()
        r = []
        for i in range(len(nums)):
            while d and nums[d[-1]] <= nums[i]:
                d.pop()
            d.append(i)
            if d[0] == i - k:
                d.popleft()
            if i >= k - 1:
                r.append(nums[d[0]])
        return r