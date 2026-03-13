class Solution:
    def maxCoins(self, nums):
        n = [1] + nums + [1]
        dp = {}
        def f(l, r):
            if l > r: return 0
            if (l, r) in dp: return dp[(l, r)]
            dp[(l, r)] = max(n[l-1] * n[k] * n[r+1] + f(l, k-1) + f(k+1, r) for k in range(l, r+1))
            return dp[(l, r)]
        return f(1, len(nums))