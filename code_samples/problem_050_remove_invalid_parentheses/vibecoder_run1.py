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
        found = False
        
        while q:
            cur = q.popleft()
            if isValid(cur):
                found = True
                break
            
            if not found:
                for i in range(len(cur)):
                    if cur[i] in '()':
                        nxt = cur[:i] + cur[i+1:]
                        if nxt not in v:
                            v.add(nxt)
                            q.append(nxt)
        
        res = []
        while q:
            cur = q.popleft()
            if isValid(cur):
                res.append(cur)
        
        if found:
            res.append(cur)
        
        return res if res else ['']