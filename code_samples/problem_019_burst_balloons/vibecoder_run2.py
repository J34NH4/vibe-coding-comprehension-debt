class Solution:
    def maxCoins(self, nums):
        n = [1] + nums + [1]
        dp = {}
        def f(l, r):
            if l > r: return 0
            if (l, r) in dp: return dp[(l, r)]
            res = 0
            for k in range(l, r + 1):
                res = max(res, n[l-1] * n[k] * n[r+1] + f(l, k-1) + f(k+1, r))
            dp[(l, r)] = res
            return res
        return f(1, len(nums))