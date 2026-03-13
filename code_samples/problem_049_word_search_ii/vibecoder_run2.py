class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Solution:
    def findWords(self, board, words):
        root = TrieNode()
        for w in words:
            n = root
            for c in w:
                if c not in n.children:
                    n.children[c] = TrieNode()
                n = n.children[c]
            n.word = w
        
        res = []
        m, n = len(board), len(board[0])
        
        def dfs(i, j, node):
            c = board[i][j]
            if c not in node.children:
                return
            node = node.children[c]
            if node.word:
                res.append(node.word)
                node.word = None
            board[i][j] = '#'
            for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, node)
            board[i][j] = c
        
        for i in range(m):
            for j in range(n):
                dfs(i, j, root)
        return res