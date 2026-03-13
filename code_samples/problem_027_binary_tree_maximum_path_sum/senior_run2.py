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
        self.global_maximum = float('-inf')
    
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """
        Find the maximum path sum in a binary tree.
        
        A path can start and end at any node in the tree.
        
        Args:
            root: Root node of the binary tree
            
        Returns:
            Maximum sum of any path in the tree
            
        Raises:
            ValueError: If root is None
        """
        if root is None:
            raise ValueError("Root cannot be None")
        
        self.global_maximum = float('-inf')
        self._calculate_max_path_contribution(root)
        return int(self.global_maximum)
    
    def _calculate_max_path_contribution(self, current_node: Optional[TreeNode]) -> int:
        """
        Calculate maximum path contribution from current node downward.
        
        This helper function calculates the maximum sum that can be obtained
        from the current node going down to any leaf, while also tracking
        the global maximum path sum that might pass through this node.
        
        Args:
            current_node: Current node being processed
            
        Returns:
            Maximum path sum from current node going downward (single path)
        """
        if current_node is None:
            return 0
        
        # Get maximum contributions from left and right subtrees
        # Use max(0, ...) to ignore negative contributions
        left_contribution = max(0, self._calculate_max_path_contribution(current_node.left))
        right_contribution = max(0, self._calculate_max_path_contribution(current_node.right))
        
        # Calculate maximum path sum that passes through current node
        # This includes both left and right subtrees (forms a "bridge")
        current_path_maximum = current_node.val + left_contribution + right_contribution
        
        # Update global maximum if current path is better
        self.global_maximum = max(self.global_maximum, current_path_maximum)
        
        # Return maximum contribution this node can provide to its parent
        # Can only choose one direction (left or right) to maintain single path
        return current_node.val + max(left_contribution, right_contribution)