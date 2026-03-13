from typing import Optional

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """Solution for Binary Tree Maximum Path Sum problem."""
    
    def __init__(self) -> None:
        """Initialize solution with global maximum tracker."""
        self.global_maximum_sum = float('-inf')
    
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """
        Find the maximum path sum in a binary tree.
        
        A path can start and end at any node in the tree.
        
        Args:
            root: The root node of the binary tree
            
        Returns:
            The maximum sum of any path in the tree
            
        Raises:
            ValueError: If the tree is empty
        """
        if not root:
            raise ValueError("Tree cannot be empty")
        
        self.global_maximum_sum = float('-inf')
        self._calculate_max_gain_from_node(root)
        return int(self.global_maximum_sum)
    
    def _calculate_max_gain_from_node(self, current_node: Optional[TreeNode]) -> int:
        """
        Calculate the maximum gain possible from a given node.
        
        This function computes two things:
        1. The maximum gain when the path goes through this node (updates global max)
        2. The maximum gain when this node is part of a path going upward
        
        Args:
            current_node: The current node being processed
            
        Returns:
            Maximum gain from this node going upward (for parent's calculation)
        """
        if not current_node:
            return 0
        
        # Get maximum gain from left and right subtrees
        # Use max(0, gain) to ignore negative paths
        left_subtree_gain = max(0, self._calculate_max_gain_from_node(current_node.left))
        right_subtree_gain = max(0, self._calculate_max_gain_from_node(current_node.right))
        
        # Calculate path sum when current node is the highest point of the path
        current_path_sum = current_node.val + left_subtree_gain + right_subtree_gain
        
        # Update global maximum if current path is better
        self.global_maximum_sum = max(self.global_maximum_sum, current_path_sum)
        
        # Return maximum gain when going upward from this node
        # Can only choose one side (left or right) when going upward
        return current_node.val + max(left_subtree_gain, right_subtree_gain)