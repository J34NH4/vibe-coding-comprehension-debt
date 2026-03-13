from typing import List, Optional, Deque
from collections import deque


class TreeNode:
    """Definition for a binary tree node."""
    
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None:
        """Initialize a tree node.
        
        Args:
            val: The value of the node
            left: Left child node
            right: Right child node
        """
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Solution for Binary Tree Level Order Traversal."""
    
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Return the level order traversal of binary tree nodes' values.
        
        Args:
            root: Root node of the binary tree
            
        Returns:
            List of lists containing node values at each level
            
        Raises:
            None: This method handles all edge cases gracefully
        """
        if not root:
            return []
        
        return self._breadth_first_traversal(root)
    
    def _breadth_first_traversal(self, root: TreeNode) -> List[List[int]]:
        """Perform breadth-first traversal to collect nodes by level.
        
        Args:
            root: Root node of the binary tree (guaranteed non-null)
            
        Returns:
            List of lists containing node values at each level
        """
        result_levels: List[List[int]] = []
        node_queue: Deque[TreeNode] = deque([root])
        
        while node_queue:
            current_level_size = len(node_queue)  # Number of nodes at current level
            current_level_values: List[int] = []
            
            # Process all nodes at the current level
            for _ in range(current_level_size):
                current_node = node_queue.popleft()
                current_level_values.append(current_node.val)
                
                # Add child nodes for next level processing
                if current_node.left:
                    node_queue.append(current_node.left)
                if current_node.right:
                    node_queue.append(current_node.right)
            
            result_levels.append(current_level_values)
        
        return result_levels