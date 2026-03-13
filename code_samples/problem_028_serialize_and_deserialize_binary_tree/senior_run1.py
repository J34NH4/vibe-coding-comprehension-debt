from typing import Optional, List
from collections import deque

class TreeNode:
    """Binary tree node definition."""
    def __init__(self, x: int) -> None:
        self.val = x
        self.left = None
        self.right = None

class Codec:
    """Codec for serializing and deserializing binary trees using preorder traversal."""
    
    NULL_MARKER = "null"
    DELIMITER = ","
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string using preorder traversal.
        
        Args:
            root: The root node of the binary tree to serialize
            
        Returns:
            A string representation of the binary tree
        """
        if not root:
            return ""
        
        serialized_values: List[str] = []
        self._serialize_preorder(root, serialized_values)
        return self.DELIMITER.join(serialized_values)
    
    def _serialize_preorder(self, node: Optional[TreeNode], values: List[str]) -> None:
        """Helper method to perform preorder traversal for serialization.
        
        Args:
            node: Current node being processed
            values: List to accumulate serialized values
        """
        if not node:
            values.append(self.NULL_MARKER)
            return
        
        values.append(str(node.val))  # Process current node
        self._serialize_preorder(node.left, values)  # Process left subtree
        self._serialize_preorder(node.right, values)  # Process right subtree

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree.
        
        Args:
            data: String representation of the binary tree
            
        Returns:
            Root node of the reconstructed binary tree
        """
        if not data:
            return None
        
        node_values = deque(data.split(self.DELIMITER))
        return self._deserialize_preorder(node_values)
    
    def _deserialize_preorder(self, values: deque) -> Optional[TreeNode]:
        """Helper method to reconstruct tree from preorder traversal values.
        
        Args:
            values: Deque containing serialized node values
            
        Returns:
            Root node of the reconstructed subtree
            
        Raises:
            IndexError: If values deque is empty when trying to process a node
        """
        if not values:
            raise IndexError("No more values available for deserialization")
        
        current_value = values.popleft()
        
        if current_value == self.NULL_MARKER:
            return None
        
        # Create current node
        current_node = TreeNode(int(current_value))
        
        # Recursively build left and right subtrees
        current_node.left = self._deserialize_preorder(values)
        current_node.right = self._deserialize_preorder(values)
        
        return current_node