from typing import Optional, List
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    """Codec for serializing and deserializing binary trees using preorder traversal."""
    
    NULL_MARKER = "null"
    DELIMITER = ","
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Serializes a tree to a single string using preorder traversal.
        
        Args:
            root: The root node of the binary tree to serialize
            
        Returns:
            A string representation of the binary tree
        """
        serialized_values = []
        self._serialize_preorder(root, serialized_values)
        return self.DELIMITER.join(serialized_values)
    
    def _serialize_preorder(self, current_node: Optional[TreeNode], serialized_values: List[str]) -> None:
        """Helper method to perform preorder traversal for serialization.
        
        Args:
            current_node: Current node being processed
            serialized_values: List to store serialized node values
        """
        if current_node is None:
            serialized_values.append(self.NULL_MARKER)
            return
        
        serialized_values.append(str(current_node.val))  # Process current node
        self._serialize_preorder(current_node.left, serialized_values)  # Process left subtree
        self._serialize_preorder(current_node.right, serialized_values)  # Process right subtree

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Deserializes string back to a binary tree.
        
        Args:
            data: String representation of the binary tree
            
        Returns:
            Root node of the reconstructed binary tree
        """
        if not data:
            return None
            
        node_values = deque(data.split(self.DELIMITER))
        return self._deserialize_preorder(node_values)
    
    def _deserialize_preorder(self, node_values: deque) -> Optional[TreeNode]:
        """Helper method to reconstruct tree from preorder traversal values.
        
        Args:
            node_values: Deque containing serialized node values
            
        Returns:
            Root node of the reconstructed subtree
        """
        if not node_values:
            return None
            
        current_value = node_values.popleft()
        
        if current_value == self.NULL_MARKER:
            return None
        
        # Create current node with the value
        current_node = TreeNode(int(current_value))
        
        # Recursively build left and right subtrees
        current_node.left = self._deserialize_preorder(node_values)
        current_node.right = self._deserialize_preorder(node_values)
        
        return current_node