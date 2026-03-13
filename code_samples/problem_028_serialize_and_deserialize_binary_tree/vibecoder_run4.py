class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    def serialize(self, root):
        if not root: return "null"
        return str(root.val) + "," + self.serialize(root.left) + "," + self.serialize(root.right)
    
    def deserialize(self, data):
        def dfs():
            v = next(vals)
            if v == "null": return None
            n = TreeNode(int(v))
            n.left = dfs()
            n.right = dfs()
            return n
        vals = iter(data.split(","))
        return dfs()