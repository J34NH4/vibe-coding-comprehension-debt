class Solution:
    def generateParentheses(self, n):
        r = []
        def f(s, o, c):
            if len(s) == 2 * n:
                r.append(s)
                return
            if o < n:
                f(s + '(', o + 1, c)
            if c < o:
                f(s + ')', o, c + 1)
        f('', 0, 0)
        return r