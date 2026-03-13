class TrieNode:
    def __init__(self):
        self.c = {}
        self.w = None

class Solution:
    def findWords(self, b, w):
        r = TrieNode()
        for word in w:
            n = r
            for c in word:
                if c not in n.c:
                    n.c[c] = TrieNode()
                n = n.c[c]
            n.w = word
        
        res = []
        
        def dfs(i, j, n):
            if i < 0 or i >= len(b) or j < 0 or j >= len(b[0]) or b[i][j] == '#':
                return
            c = b[i][j]
            if c not in n.c:
                return
            n = n.c[c]
            if n.w:
                res.append(n.w)
                n.w = None
            b[i][j] = '#'
            dfs(i+1, j, n)
            dfs(i-1, j, n)
            dfs(i, j+1, n)
            dfs(i, j-1, n)
            b[i][j] = c
        
        for i in range(len(b)):
            for j in range(len(b[0])):
                dfs(i, j, r)
        
        return res