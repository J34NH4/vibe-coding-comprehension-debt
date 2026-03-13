class Solution:
    def combinationSum(self, c, t):
        r = []
        def f(i, p, s):
            if s == t:
                r.append(p[:])
                return
            if s > t or i >= len(c):
                return
            p.append(c[i])
            f(i, p, s + c[i])
            p.pop()
            f(i + 1, p, s)
        f(0, [], 0)
        return r