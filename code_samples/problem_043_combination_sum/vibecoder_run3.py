class Solution:
    def combinationSum(self, c, t):
        r = []
        def bt(i, p, s):
            if s == t:
                r.append(p[:])
                return
            if s > t or i >= len(c):
                return
            p.append(c[i])
            bt(i, p, s + c[i])
            p.pop()
            bt(i + 1, p, s)
        bt(0, [], 0)
        return r