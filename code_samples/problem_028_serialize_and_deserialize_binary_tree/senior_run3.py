from typing import Optional, List
from collections import deque

class TreeNode:
    """Binary tree node definition."""
    
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Codec:
    """Codec for serializing and deserializing binary trees using preorder traversal."""
    
    NULL_MARKER: str = "null"
    DELIMITER: str = ","

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string using preorder traversal.
        
        Args:
            root: Root node of the binary tree to serialize.
            
        Returns:
            String representation of the binary tree.
        """
        if not root:
            return ""
        
        serialized_values: List[str] = []
        self._serialize_preorder(root, serialized_values)
        return self.DELIMITER.join(serialized_values)
    
    def _serialize_preorder(self, current_node: Optional[TreeNode], serialized_values: List[str]) -> None:
        """Helper method to serialize tree using preorder traversal.
        
        Args:
            current_node: Current node being processed.
            serialized_values: List to store serialized node values.
        """
        if not current_node:
            serialized_values.append(self.NULL_MARKER)
            return
        
        serialized_values.append(str(current_node.val))  # Process current node
        self._serialize_preorder(current_node.left, serialized_values)  # Process left subtree
        self._serialize_preorder(current_node.right, serialized_values)  # Process right subtree

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree.
        
        Args:
            data: String representation of the binary tree.
            
        Returns:
            Root node of the reconstructed binary tree.
        """
        if not data:
            return None
        
        node_values: List[str] = data.split(self.DELIMITER)
        value_queue: deque = deque(node_values)
        return self._deserialize_preorder(value_queue)
    
    def _deserialize_preorder(self, value_queue: deque) -> Optional[TreeNode]:
        """Helper method to deserialize tree using preorder traversal.
        
        Args:
            value_queue: Queue containing serialized node values.
            
        Returns:
            Root node of the current subtree.
        """
        if not value_queue:
            return None
        
        current_value: str = value_queue.popleft()
        
        if current_value == self.NULL_MARKER:  # Handle null nodes
            return None
        
        try:
            node_value: int = int(current_value)
        except ValueError:
            return None
        
        current_node: TreeNode = TreeNode(node_value)  # Create current node
        current_node.left = self._deserialize_preorder(value_queue)  # Build left subtree
        current_node.right = self._deserialize_preorder(value_queue)  # Build right subtree
        
        return current_node