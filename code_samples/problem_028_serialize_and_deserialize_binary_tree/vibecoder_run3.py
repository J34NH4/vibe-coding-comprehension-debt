class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root):
        def dfs(n):
            return str(n.val) + ',' + dfs(n.left) + ',' + dfs(n.right) if n else '#,'
        return dfs(root)[:-1]
    
    def deserialize(self, data):
        def dfs():
            v = next(it)
            return TreeNode(int(v), dfs(), dfs()) if v != '#' else None
        it = iter(data.split(','))
        return dfs()