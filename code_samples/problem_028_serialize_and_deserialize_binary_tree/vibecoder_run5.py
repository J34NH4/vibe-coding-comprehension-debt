class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    def serialize(self, root):
        def dfs(n):
            if not n: return "null,"
            return str(n.val) + "," + dfs(n.left) + dfs(n.right)
        return dfs(root)
    
    def deserialize(self, data):
        def dfs():
            v = next(vals)
            if v == "null": return None
            n = TreeNode(int(v))
            n.left = dfs()
            n.right = dfs()
            return n
        vals = iter(data.split(','))
        return dfs()