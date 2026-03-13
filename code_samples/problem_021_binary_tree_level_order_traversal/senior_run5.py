from typing import List, Optional, Deque
from collections import deque

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Returns the level order traversal of a binary tree.
        
        Uses BFS with a queue to traverse nodes level by level, collecting
        values at each level into separate lists.
        
        Args:
            root: The root node of the binary tree
            
        Returns:
            A list of lists where each inner list contains the values of nodes
            at that level from left to right
            
        Time Complexity: O(n) where n is the number of nodes
        Space Complexity: O(w) where w is the maximum width of the tree
        """
        if not root:
            return []
        
        result: List[List[int]] = []
        node_queue: Deque[TreeNode] = deque([root])
        
        while node_queue:
            current_level_size = len(node_queue)  # Number of nodes at current level
            current_level_values: List[int] = []
            
            # Process all nodes at the current level
            for _ in range(current_level_size):
                current_node = node_queue.popleft()
                current_level_values.append(current_node.val)
                
                # Add child nodes to queue for next level processing
                if current_node.left:
                    node_queue.append(current_node.left)
                if current_node.right:
                    node_queue.append(current_node.right)
            
            result.append(current_level_values)
        
        return result