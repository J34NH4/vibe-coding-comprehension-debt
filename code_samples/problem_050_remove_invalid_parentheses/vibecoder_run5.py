from collections import deque

class Solution:
    def removeInvalidParentheses(self, s):
        def isValid(x):
            c = 0
            for ch in x:
                if ch == '(':
                    c += 1
                elif ch == ')':
                    c -= 1
                    if c < 0:
                        return False
            return c == 0
        
        q = deque([s])
        v = {s}
        f = False
        
        while q:
            x = q.popleft()
            if isValid(x):
                f = True
                yield x
            if not f:
                for i in range(len(x)):
                    if x[i] in '()':
                        n = x[:i] + x[i+1:]
                        if n not in v:
                            v.add(n)
                            q.append(n)