from typing import Optional, Tuple

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None) -> None:
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
            root: The root of the binary tree
            
        Returns:
            The maximum path sum as an integer
            
        Raises:
            ValueError: If root is None
        """
        if root is None:
            raise ValueError("Root cannot be None")
        
        maximum_path_sum = float('-inf')
        
        def calculate_max_gain(current_node: Optional[TreeNode]) -> int:
            """
            Calculate the maximum gain from a subtree rooted at current_node.
            
            This function also updates the global maximum_path_sum.
            
            Args:
                current_node: The current node being processed
                
            Returns:
                Maximum gain that can be obtained by including current_node
                in a path that extends upward to its parent
            """
            nonlocal maximum_path_sum
            
            if current_node is None:
                return 0
            
            # Calculate maximum gain from left and right subtrees
            # Use max(0, gain) to ignore negative contributions
            left_subtree_gain = max(0, calculate_max_gain(current_node.left))
            right_subtree_gain = max(0, calculate_max_gain(current_node.right))
            
            # Calculate the maximum path sum that passes through current_node
            current_path_sum = current_node.val + left_subtree_gain + right_subtree_gain
            
            # Update global maximum if current path is better
            maximum_path_sum = max(maximum_path_sum, current_path_sum)
            
            # Return the maximum gain that can be extended upward
            # Can only choose one branch (left or right) when extending upward
            return current_node.val + max(left_subtree_gain, right_subtree_gain)
        
        calculate_max_gain(root)
        return int(maximum_path_sum)