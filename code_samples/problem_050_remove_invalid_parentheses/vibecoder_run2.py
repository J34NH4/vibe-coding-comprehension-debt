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
        v = set([s])
        f = False
        
        while q:
            x = q.popleft()
            if isValid(x):
                f = True
                yield x
            if f:
                continue
            for i in range(len(x)):
                if x[i] in '()':
                    y = x[:i] + x[i+1:]
                    if y not in v:
                        v.add(y)
                        q.append(y)