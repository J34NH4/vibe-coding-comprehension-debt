class Solution:
    def generateParentheses(self, n: int) -> List[str]:
        r = []
        def bt(s, o, c):
            if len(s) == 2 * n:
                r.append(s)
                return
            if o < n: bt(s + '(', o + 1, c)
            if c < o: bt(s + ')', o, c + 1)
        bt('', 0, 0)
        return r