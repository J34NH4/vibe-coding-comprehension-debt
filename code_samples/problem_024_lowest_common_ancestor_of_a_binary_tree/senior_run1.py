from typing import Optional

class TreeNode:
    """Definition for a binary tree node."""
    
    def __init__(self, x: int) -> None:
        self.val = x
        self.left = None
        self.right = None

class Solution:
    """Solution for finding the lowest common ancestor of two nodes in a binary tree."""
    
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Finds the lowest common ancestor of two nodes in a binary tree.
        
        Args:
            root: The root of the binary tree
            p: First target node
            q: Second target node
            
        Returns:
            The lowest common ancestor node of p and q
            
        Raises:
            ValueError: If root is None or p/q are not found in the tree
        """
        if not root:
            raise ValueError("Root cannot be None")
            
        return self._find_lca_recursive(root, p, q)
    
    def _find_lca_recursive(self, current_node: Optional[TreeNode], target_p: TreeNode, target_q: TreeNode) -> Optional[TreeNode]:
        """
        Recursively searches for the lowest common ancestor.
        
        Args:
            current_node: Current node being examined
            target_p: First target node to find
            target_q: Second target node to find
            
        Returns:
            The LCA node if found, None otherwise
        """
        # Base case: reached leaf or found one of the targets
        if not current_node or current_node == target_p or current_node == target_q:
            return current_node
        
        # Search in left and right subtrees
        left_result = self._find_lca_recursive(current_node.left, target_p, target_q)
        right_result = self._find_lca_recursive(current_node.right, target_p, target_q)
        
        # If both targets found in different subtrees, current node is LCA
        if left_result and right_result:
            return current_node
        
        # Return whichever subtree contains a target (or None if neither)
        return left_result if left_result else right_result