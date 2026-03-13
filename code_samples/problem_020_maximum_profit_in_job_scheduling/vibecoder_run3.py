class Solution:
    def jobScheduling(self, startTime, endTime, profit):
        j = sorted(zip(endTime, startTime, profit))
        dp = [0]
        e = [0]
        for end, start, p in j:
            i = self.bs(e, start)
            if dp[i] + p > dp[-1]:
                dp.append(dp[i] + p)
                e.append(end)
        return dp[-1]
    
    def bs(self, arr, x):
        l, r = 0, len(arr) - 1
        while l <= r:
            m = (l + r) // 2
            if arr[m] <= x:
                l = m + 1
            else:
                r = m - 1
        return r