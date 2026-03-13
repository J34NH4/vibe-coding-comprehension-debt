from typing import Optional, List
from collections import deque

class TreeNode:
    """Binary tree node definition."""
    
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

class Codec:
    """Codec for serializing and deserializing binary trees using level-order traversal."""
    
    NULL_MARKER = "null"
    DELIMITER = ","
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string using level-order traversal.
        
        Args:
            root: Root node of the binary tree
            
        Returns:
            String representation of the tree
        """
        if not root:
            return self.NULL_MARKER
            
        serialized_values: List[str] = []
        node_queue: deque = deque([root])
        
        while node_queue:
            current_node = node_queue.popleft()
            
            if current_node:
                serialized_values.append(str(current_node.val))
                node_queue.append(current_node.left)  # May be None
                node_queue.append(current_node.right)  # May be None
            else:
                serialized_values.append(self.NULL_MARKER)
        
        # Remove trailing null markers to optimize string length
        while serialized_values and serialized_values[-1] == self.NULL_MARKER:
            serialized_values.pop()
            
        return self.DELIMITER.join(serialized_values)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree.
        
        Args:
            data: String representation of the tree
            
        Returns:
            Root node of the reconstructed binary tree
        """
        if not data or data == self.NULL_MARKER:
            return None
            
        node_values = data.split(self.DELIMITER)
        
        try:
            root_value = int(node_values[0])
        except (ValueError, IndexError):
            return None
            
        root_node = TreeNode(root_value)
        node_queue: deque = deque([root_node])
        value_index = 1
        
        while node_queue and value_index < len(node_values):
            current_node = node_queue.popleft()
            
            # Process left child
            if value_index < len(node_values):
                left_value = node_values[value_index]
                value_index += 1
                
                if left_value != self.NULL_MARKER:
                    try:
                        left_node = TreeNode(int(left_value))
                        current_node.left = left_node
                        node_queue.append(left_node)
                    except ValueError:
                        pass  # Skip invalid values
            
            # Process right child
            if value_index < len(node_values):
                right_value = node_values[value_index]
                value_index += 1
                
                if right_value != self.NULL_MARKER:
                    try:
                        right_node = TreeNode(int(right_value))
                        current_node.right = right_node
                        node_queue.append(right_node)
                    except ValueError:
                        pass  # Skip invalid values
        
        return root_node