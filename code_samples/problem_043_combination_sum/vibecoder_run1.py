class Solution:
    def combinationSum(self, c, t):
        r = []
        def b(i, p, s):
            if s == t:
                r.append(p[:])
                return
            if s > t or i >= len(c):
                return
            p.append(c[i])
            b(i, p, s + c[i])
            p.pop()
            b(i + 1, p, s)
        b(0, [], 0)
        return r