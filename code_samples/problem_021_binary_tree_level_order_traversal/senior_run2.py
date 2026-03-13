from typing import List, Optional
from collections import deque

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """Solution for Binary Tree Level Order Traversal problem."""
    
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Performs level order traversal of a binary tree.
        
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
        nodes_queue: deque[TreeNode] = deque([root])
        
        while nodes_queue:
            current_level_size: int = len(nodes_queue)
            current_level_values: List[int] = []
            
            # Process all nodes at current level
            for _ in range(current_level_size):
                current_node: TreeNode = nodes_queue.popleft()
                current_level_values.append(current_node.val)
                
                # Add child nodes to queue for next level
                if current_node.left:
                    nodes_queue.append(current_node.left)
                if current_node.right:
                    nodes_queue.append(current_node.right)
            
            result_levels.append(current_level_values)
        
        return result_levels