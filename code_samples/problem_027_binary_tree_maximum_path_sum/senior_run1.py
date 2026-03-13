from typing import Optional

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """Solution for Binary Tree Maximum Path Sum problem."""
    
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """
        Find the maximum path sum in a binary tree.
        
        A path can start and end at any node in the tree.
        
        Args:
            root: The root node of the binary tree
            
        Returns:
            The maximum sum of any path in the tree
            
        Raises:
            ValueError: If root is None
        """
        if root is None:
            raise ValueError("Root cannot be None")
            
        self.maximum_path_sum = float('-inf')  # Global maximum tracker
        self._calculate_max_gain(root)
        return int(self.maximum_path_sum)
    
    def _calculate_max_gain(self, current_node: Optional[TreeNode]) -> int:
        """
        Calculate the maximum gain from a subtree rooted at current_node.
        
        This function serves dual purposes:
        1. Updates the global maximum path sum considering paths through current_node
        2. Returns the maximum gain that can be obtained by including current_node
           in a path that continues upward to its parent
        
        Args:
            current_node: The current node being processed
            
        Returns:
            Maximum gain that can be obtained by including current_node in an upward path
        """
        if current_node is None:
            return 0
            
        # Calculate maximum gain from left and right subtrees
        # Use max(0, gain) to ignore negative contributions
        left_subtree_gain = max(0, self._calculate_max_gain(current_node.left))
        right_subtree_gain = max(0, self._calculate_max_gain(current_node.right))
        
        # Calculate the maximum path sum that passes through current_node
        current_path_sum = current_node.val + left_subtree_gain + right_subtree_gain
        
        # Update global maximum if current path is better
        self.maximum_path_sum = max(self.maximum_path_sum, current_path_sum)
        
        # Return the maximum gain for paths continuing upward
        # Can only choose one branch (left or right) when going upward
        return current_node.val + max(left_subtree_gain, right_subtree_gain)