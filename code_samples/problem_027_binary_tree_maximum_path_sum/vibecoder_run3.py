class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root):
        self.m = float('-inf')
        def h(n):
            if not n: return 0
            l = max(0, h(n.left))
            r = max(0, h(n.right))
            self.m = max(self.m, n.val + l + r)
            return n.val + max(l, r)
        h(root)
        return self.m