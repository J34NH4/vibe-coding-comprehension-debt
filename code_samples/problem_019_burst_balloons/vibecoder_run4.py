class Solution:
    def maxCoins(self, nums):
        n = [1] + [x for x in nums if x > 0] + [1]
        m = {}
        def dp(l, r):
            if l + 1 == r: return 0
            if (l, r) in m: return m[(l, r)]
            res = 0
            for k in range(l + 1, r):
                res = max(res, n[l] * n[k] * n[r] + dp(l, k) + dp(k, r))
            m[(l, r)] = res
            return res
        return dp(0, len(n) - 1)