from collections import deque
from typing import List, Optional


class TreeNode:
    """Definition for a binary tree node."""
    
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Solution for Binary Tree Level Order Traversal problem."""
    
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Performs level order traversal of a binary tree using BFS.
        
        Args:
            root: The root node of the binary tree
            
        Returns:
            A list of lists containing node values at each level
            
        Raises:
            None
        """
        if not root:
            return []
        
        result_levels: List[List[int]] = []
        current_level_queue: deque = deque([root])
        
        while current_level_queue:
            current_level_size = len(current_level_queue)  # Number of nodes at current level
            current_level_values: List[int] = []
            
            # Process all nodes at the current level
            for _ in range(current_level_size):
                current_node = current_level_queue.popleft()
                current_level_values.append(current_node.val)
                
                # Add child nodes to queue for next level processing
                if current_node.left:
                    current_level_queue.append(current_node.left)
                if current_node.right:
                    current_level_queue.append(current_node.right)
            
            result_levels.append(current_level_values)
        
        return result_levels