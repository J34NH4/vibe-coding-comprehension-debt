from typing import Optional, List
from collections import deque

class TreeNode:
    """Binary tree node representation."""
    
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None:
        """Initialize a tree node with value and optional left/right children.
        
        Args:
            val: The value stored in this node
            left: Optional left child node
            right: Optional right child node
        """
        self.val = val
        self.left = left
        self.right = right

class Codec:
    """Codec for serializing and deserializing binary trees using preorder traversal."""
    
    NULL_MARKER = "null"
    DELIMITER = ","
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string using preorder traversal.
        
        Args:
            root: Root node of the binary tree to serialize
            
        Returns:
            String representation of the binary tree
        """
        serialized_values: List[str] = []
        
        def preorder_serialize(current_node: Optional[TreeNode]) -> None:
            """Perform preorder traversal and collect node values.
            
            Args:
                current_node: Current node being processed
            """
            if current_node is None:
                serialized_values.append(self.NULL_MARKER)
                return
            
            serialized_values.append(str(current_node.val))  # Process current node
            preorder_serialize(current_node.left)  # Traverse left subtree
            preorder_serialize(current_node.right)  # Traverse right subtree
        
        preorder_serialize(root)
        return self.DELIMITER.join(serialized_values)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree.
        
        Args:
            data: String representation of the binary tree
            
        Returns:
            Root node of the reconstructed binary tree
            
        Raises:
            ValueError: If the serialized data is malformed
        """
        if not data:
            raise ValueError("Cannot deserialize empty data")
        
        node_values = deque(data.split(self.DELIMITER))
        
        def preorder_deserialize() -> Optional[TreeNode]:
            """Reconstruct tree using preorder traversal.
            
            Returns:
                Root node of the reconstructed subtree
                
            Raises:
                ValueError: If no more values available during reconstruction
            """
            if not node_values:
                raise ValueError("Insufficient data for tree reconstruction")
            
            current_value = node_values.popleft()
            
            if current_value == self.NULL_MARKER:
                return None
            
            try:
                node_val = int(current_value)
            except ValueError:
                raise ValueError(f"Invalid node value: {current_value}")
            
            current_node = TreeNode(node_val)  # Create current node
            current_node.left = preorder_deserialize()  # Reconstruct left subtree
            current_node.right = preorder_deserialize()  # Reconstruct right subtree
            
            return current_node
        
        return preorder_deserialize()