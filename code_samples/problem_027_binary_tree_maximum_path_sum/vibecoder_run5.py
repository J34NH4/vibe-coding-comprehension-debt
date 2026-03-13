class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root):
        self.m = float('-inf')
        def d(n):
            if not n: return 0
            l = max(0, d(n.left))
            r = max(0, d(n.right))
            self.m = max(self.m, n.val + l + r)
            return n.val + max(l, r)
        d(root)
        return self.m