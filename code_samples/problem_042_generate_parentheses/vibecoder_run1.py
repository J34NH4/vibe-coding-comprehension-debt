class Solution:
    def generateParentheses(self, n):
        r = []
        def b(s, o, c):
            if len(s) == 2 * n:
                r.append(s)
                return
            if o < n:
                b(s + '(', o + 1, c)
            if c < o:
                b(s + ')', o, c + 1)
        b('', 0, 0)
        return r