class Solution:
    def combinationSum(self, candidates, target):
        r = []
        def bt(i, c, s):
            if s == target:
                r.append(c[:])
                return
            if s > target or i == len(candidates):
                return
            c.append(candidates[i])
            bt(i, c, s + candidates[i])
            c.pop()
            bt(i + 1, c, s)
        bt(0, [], 0)
        return r