from typing import Dict, Optional

class Node:
    """Doubly linked list node representing a count value and associated keys."""
    
    def __init__(self, count: int) -> None:
        """Initialize node with given count.
        
        Args:
            count: The frequency count this node represents
        """
        self.count = count
        self.keys = set()  # Keys with this count
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class AllOne:
    """Data structure supporting O(1) increment, decrement, and min/max key operations."""
    
    def __init__(self) -> None:
        """Initialize the data structure."""
        self.key_to_node: Dict[str, Node] = {}  # Map key to its count node
        
        # Create dummy head and tail nodes for easier list manipulation
        self.head = Node(0)  # Dummy head with count 0
        self.tail = Node(0)  # Dummy tail with count 0
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node_after(self, prev_node: Node, new_node: Node) -> None:
        """Insert new_node after prev_node in the doubly linked list.
        
        Args:
            prev_node: Node after which to insert
            new_node: Node to insert
        """
        next_node = prev_node.next
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = next_node
        next_node.prev = new_node

    def _remove_node(self, node: Node) -> None:
        """Remove node from the doubly linked list.
        
        Args:
            node: Node to remove
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _get_or_create_node(self, target_count: int, reference_node: Node, after: bool) -> Node:
        """Get existing node with target_count or create new one at specified position.
        
        Args:
            target_count: The count value needed
            reference_node: Node to position relative to
            after: If True, create after reference_node; if False, create before
            
        Returns:
            Node with the target count
        """
        expected_node = reference_node.next if after else reference_node.prev
        
        if expected_node.count == target_count:
            return expected_node
        
        # Create new node at the correct position
        new_node = Node(target_count)
        if after:
            self._add_node_after(reference_node, new_node)
        else:
            self._add_node_after(expected_node, new_node)
        
        return new_node

    def inc(self, key: str) -> None:
        """Increment the count of the given key by 1.
        
        Args:
            key: Key to increment
        """
        if key in self.key_to_node:
            current_node = self.key_to_node[key]
            target_count = current_node.count + 1
            
            # Get or create node for target count
            target_node = self._get_or_create_node(target_count, current_node, after=True)
            
            # Move key from current node to target node
            current_node.keys.remove(key)
            target_node.keys.add(key)
            self.key_to_node[key] = target_node
            
            # Remove current node if it becomes empty
            if not current_node.keys:
                self._remove_node(current_node)
        else:
            # New key with count 1
            target_node = self._get_or_create_node(1, self.head, after=True)
            target_node.keys.add(key)
            self.key_to_node[key] = target_node

    def dec(self, key: str) -> None:
        """Decrement the count of the given key by 1.
        
        Args:
            key: Key to decrement
        """
        if key not in self.key_to_node:
            return
        
        current_node = self.key_to_node[key]
        current_count = current_node.count
        
        # Remove key from current node
        current_node.keys.remove(key)
        
        if current_count == 1:
            # Remove key entirely when count reaches 0
            del self.key_to_node[key]
        else:
            # Move key to node with count-1
            target_count = current_count - 1
            target_node = self._get_or_create_node(target_count, current_node, after=False)
            target_node.keys.add(key)
            self.key_to_node[key] = target_node
        
        # Remove current node if it becomes empty
        if not current_node.keys:
            self._remove_node(current_node)

    def getMaxKey(self) -> str:
        """Get one of the keys with the maximum count.
        
        Returns:
            A key with maximum count, or empty string if no keys exist
        """
        if self.tail.prev == self.head:  # No nodes between head and tail
            return ""
        
        max_node = self.tail.prev
        return next(iter(max_node.keys))  # Return any key from the set

    def getMinKey(self) -> str:
        """Get one of the keys with the minimum count.
        
        Returns:
            A key with minimum count, or empty string if no keys exist
        """
        if self.head.next == self.tail:  # No nodes between head and tail
            return ""
        
        min_node = self.head.next
        return next(iter(min_node.keys))  # Return any key from the set