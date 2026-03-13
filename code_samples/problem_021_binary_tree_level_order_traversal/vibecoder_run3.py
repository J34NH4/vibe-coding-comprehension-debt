from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root):
        if not root: return []
        r, q = [], deque([root])
        while q:
            r.append([n.val for n in q])
            q = deque([c for n in q for c in [n.left, n.right] if c])
        return r