from typing import Optional

class TreeNode:
    """Definition for a binary tree node."""
    
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None:
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
            The maximum path sum as an integer
            
        Raises:
            ValueError: If root is None
        """
        if root is None:
            raise ValueError("Root cannot be None")
        
        self.global_maximum_sum = float('-inf')
        self._calculate_maximum_path_from_node(root)
        return int(self.global_maximum_sum)
    
    def _calculate_maximum_path_from_node(self, current_node: Optional[TreeNode]) -> int:
        """
        Calculate the maximum path sum starting from current node going down.
        
        This is a helper function that uses post-order traversal to calculate
        the maximum path sum that can be achieved starting from the current node
        and going down through its descendants.
        
        Args:
            current_node: The current node being processed
            
        Returns:
            Maximum path sum from current node going down (single direction)
        """
        if current_node is None:
            return 0
        
        # Calculate maximum path sums from left and right subtrees
        # Use max with 0 to ignore negative contributions
        left_maximum_contribution = max(0, self._calculate_maximum_path_from_node(current_node.left))
        right_maximum_contribution = max(0, self._calculate_maximum_path_from_node(current_node.right))
        
        # Calculate maximum path sum that passes through current node
        current_path_maximum = current_node.val + left_maximum_contribution + right_maximum_contribution
        
        # Update global maximum if current path is better
        self.global_maximum_sum = max(self.global_maximum_sum, current_path_maximum)
        
        # Return maximum path sum from current node going down (single direction)
        # This can only include one subtree to maintain valid path structure
        return current_node.val + max(left_maximum_contribution, right_maximum_contribution)