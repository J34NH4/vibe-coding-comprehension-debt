from typing import Dict, Optional

class Node:
    """A doubly linked list node containing a frequency count and keys with that count."""
    
    def __init__(self, count: int = 0) -> None:
        """Initialize a node with given count.
        
        Args:
            count: The frequency count for this node.
        """
        self.count: int = count
        self.keys: set = set()
        self.previous_node: Optional['Node'] = None
        self.next_node: Optional['Node'] = None

class AllOne:
    """Data structure supporting O(1) increment, decrement, and min/max key operations."""
    
    def __init__(self) -> None:
        """Initialize the data structure with sentinel head and tail nodes."""
        self.key_to_node: Dict[str, Node] = {}  # Maps key to its count node
        self.head_sentinel: Node = Node(0)  # Dummy head for easier operations
        self.tail_sentinel: Node = Node(0)  # Dummy tail for easier operations
        self.head_sentinel.next_node = self.tail_sentinel
        self.tail_sentinel.previous_node = self.head_sentinel

    def inc(self, key: str) -> None:
        """Increment the count of the given key by 1.
        
        Args:
            key: The key to increment.
        """
        if key in self.key_to_node:
            current_node = self.key_to_node[key]
            self._move_key_to_next_count(key, current_node)
        else:
            # Key doesn't exist, add it with count 1
            first_node = self.head_sentinel.next_node
            if first_node.count == 1:
                first_node.keys.add(key)
                self.key_to_node[key] = first_node
            else:
                new_node = self._create_node_after(self.head_sentinel, 1)
                new_node.keys.add(key)
                self.key_to_node[key] = new_node

    def dec(self, key: str) -> None:
        """Decrement the count of the given key by 1.
        
        Args:
            key: The key to decrement.
        """
        if key not in self.key_to_node:
            return
        
        current_node = self.key_to_node[key]
        
        if current_node.count == 1:
            # Remove key entirely when count reaches 0
            current_node.keys.remove(key)
            del self.key_to_node[key]
        else:
            # Move key to previous count
            self._move_key_to_previous_count(key, current_node)
        
        # Clean up empty node
        if not current_node.keys:
            self._remove_node(current_node)

    def getMaxKey(self) -> str:
        """Get a key with maximum count.
        
        Returns:
            A key with the maximum count, or empty string if no keys exist.
        """
        if self.tail_sentinel.previous_node == self.head_sentinel:
            return ""
        return next(iter(self.tail_sentinel.previous_node.keys))

    def getMinKey(self) -> str:
        """Get a key with minimum count.
        
        Returns:
            A key with the minimum count, or empty string if no keys exist.
        """
        if self.head_sentinel.next_node == self.tail_sentinel:
            return ""
        return next(iter(self.head_sentinel.next_node.keys))

    def _move_key_to_next_count(self, key: str, current_node: Node) -> None:
        """Move a key from current node to the next count node.
        
        Args:
            key: The key to move.
            current_node: The current node containing the key.
        """
        target_count = current_node.count + 1
        next_node = current_node.next_node
        
        # Check if next node has the target count
        if next_node.count == target_count:
            target_node = next_node
        else:
            # Create new node with target count
            target_node = self._create_node_after(current_node, target_count)
        
        # Move key to target node
        current_node.keys.remove(key)
        target_node.keys.add(key)
        self.key_to_node[key] = target_node
        
        # Remove current node if empty
        if not current_node.keys:
            self._remove_node(current_node)

    def _move_key_to_previous_count(self, key: str, current_node: Node) -> None:
        """Move a key from current node to the previous count node.
        
        Args:
            key: The key to move.
            current_node: The current node containing the key.
        """
        target_count = current_node.count - 1
        previous_node = current_node.previous_node
        
        # Check if previous node has the target count
        if previous_node.count == target_count:
            target_node = previous_node
        else:
            # Create new node with target count
            target_node = self._create_node_before(current_node, target_count)
        
        # Move key to target node
        current_node.keys.remove(key)
        target_node.keys.add(key)
        self.key_to_node[key] = target_node

    def _create_node_after(self, node: Node, count: int) -> Node:
        """Create a new node with given count after the specified node.
        
        Args:
            node: The node after which to insert the new node.
            count: The count for the new node.
            
        Returns:
            The newly created node.
        """
        new_node = Node(count)
        new_node.previous_node = node
        new_node.next_node = node.next_node
        node.next_node.previous_node = new_node
        node.next_node = new_node
        return new_node

    def _create_node_before(self, node: Node, count: int) -> Node:
        """Create a new node with given count before the specified node.
        
        Args:
            node: The node before which to insert the new node.
            count: The count for the new node.
            
        Returns:
            The newly created node.
        """
        new_node = Node(count)
        new_node.next_node = node
        new_node.previous_node = node.previous_node
        node.previous_node.next_node = new_node
        node.previous_node = new_node
        return new_node

    def _remove_node(self, node: Node) -> None:
        """Remove a node from the doubly linked list.
        
        Args:
            node: The node to remove.
        """
        node.previous_node.next_node = node.next_node
        node.next_node.previous_node = node.previous_node