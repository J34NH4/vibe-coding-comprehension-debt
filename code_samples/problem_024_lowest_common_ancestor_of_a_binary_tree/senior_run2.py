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
        Find the lowest common ancestor of two nodes in a binary tree.
        
        Args:
            root: The root of the binary tree
            p: First target node
            q: Second target node
            
        Returns:
            The lowest common ancestor node of p and q
            
        Raises:
            ValueError: If root is None or if p or q are not found in the tree
        """
        if root is None:
            raise ValueError("Root cannot be None")
            
        result = self._find_lca_recursive(root, p, q)
        if result is None:
            raise ValueError("One or both nodes not found in the tree")
            
        return result
    
    def _find_lca_recursive(self, current_node: Optional[TreeNode], target_p: TreeNode, target_q: TreeNode) -> Optional[TreeNode]:
        """
        Recursively find the lowest common ancestor using post-order traversal.
        
        Args:
            current_node: Current node being processed
            target_p: First target node to find
            target_q: Second target node to find
            
        Returns:
            The LCA node if found, None otherwise
        """
        # Base case: reached end of branch or found one of the targets
        if current_node is None or current_node == target_p or current_node == target_q:
            return current_node
        
        # Search in left and right subtrees
        left_result = self._find_lca_recursive(current_node.left, target_p, target_q)
        right_result = self._find_lca_recursive(current_node.right, target_p, target_q)
        
        # If both subtrees return non-null, current node is the LCA
        if left_result is not None and right_result is not None:
            return current_node
        
        # Return whichever subtree found a target node (or None if neither did)
        return left_result if left_result is not None else right_result