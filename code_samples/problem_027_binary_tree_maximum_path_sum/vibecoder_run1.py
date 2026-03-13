class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root):
        self.res = float('-inf')
        def dfs(node):
            if not node: return 0
            l = max(0, dfs(node.left))
            r = max(0, dfs(node.right))
            self.res = max(self.res, node.val + l + r)
            return node.val + max(l, r)
        dfs(root)
        return self.res