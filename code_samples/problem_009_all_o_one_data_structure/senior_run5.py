from typing import Dict, Optional

class Node:
    """Doubly linked list node representing a frequency bucket."""
    
    def __init__(self, frequency: int) -> None:
        """Initialize a node with given frequency.
        
        Args:
            frequency: The count value for this bucket
        """
        self.frequency: int = frequency
        self.keys: set = set()  # Keys with this frequency
        self.previous: Optional[Node] = None
        self.next: Optional[Node] = None

class AllOne:
    """Data structure supporting O(1) increment, decrement, and min/max key operations."""

    def __init__(self) -> None:
        """Initialize the AllOne data structure."""
        self.key_to_node: Dict[str, Node] = {}  # Maps key to its frequency node
        
        # Create sentinel nodes for easier list manipulation
        self.head: Node = Node(0)  # Dummy head (minimum frequency side)
        self.tail: Node = Node(0)  # Dummy tail (maximum frequency side)
        self.head.next = self.tail
        self.tail.previous = self.head

    def _insert_after(self, previous_node: Node, frequency: int) -> Node:
        """Insert a new node with given frequency after the specified node.
        
        Args:
            previous_node: Node after which to insert
            frequency: Frequency value for the new node
            
        Returns:
            The newly created and inserted node
        """
        new_node = Node(frequency)
        new_node.next = previous_node.next
        new_node.previous = previous_node
        previous_node.next.previous = new_node
        previous_node.next = new_node
        return new_node

    def _remove_node(self, node: Node) -> None:
        """Remove a node from the doubly linked list.
        
        Args:
            node: Node to remove from the list
        """
        node.previous.next = node.next
        node.next.previous = node.previous

    def inc(self, key: str) -> None:
        """Increment the count of the given key by 1.
        
        Args:
            key: The key to increment
        """
        if key in self.key_to_node:
            current_node = self.key_to_node[key]
            target_frequency = current_node.frequency + 1
            
            # Find or create target frequency node
            if current_node.next.frequency == target_frequency:
                target_node = current_node.next
            else:
                target_node = self._insert_after(current_node, target_frequency)
            
            # Move key to target frequency
            target_node.keys.add(key)
            self.key_to_node[key] = target_node
            
            # Clean up current node
            current_node.keys.remove(key)
            if not current_node.keys:
                self._remove_node(current_node)
        else:
            # New key starts with frequency 1
            if self.head.next.frequency == 1:
                target_node = self.head.next
            else:
                target_node = self._insert_after(self.head, 1)
            
            target_node.keys.add(key)
            self.key_to_node[key] = target_node

    def dec(self, key: str) -> None:
        """Decrement the count of the given key by 1.
        
        Args:
            key: The key to decrement
        """
        if key not in self.key_to_node:
            return
        
        current_node = self.key_to_node[key]
        
        if current_node.frequency == 1:
            # Remove key completely
            del self.key_to_node[key]
        else:
            target_frequency = current_node.frequency - 1
            
            # Find or create target frequency node
            if current_node.previous.frequency == target_frequency:
                target_node = current_node.previous
            else:
                target_node = self._insert_after(current_node.previous, target_frequency)
            
            # Move key to target frequency
            target_node.keys.add(key)
            self.key_to_node[key] = target_node
        
        # Clean up current node
        current_node.keys.remove(key)
        if not current_node.keys:
            self._remove_node(current_node)

    def getMaxKey(self) -> str:
        """Get one of the keys with the maximum count.
        
        Returns:
            A key with maximum count, or empty string if no keys exist
        """
        if self.tail.previous == self.head:
            return ""
        return next(iter(self.tail.previous.keys))

    def getMinKey(self) -> str:
        """Get one of the keys with the minimum count.
        
        Returns:
            A key with minimum count, or empty string if no keys exist
        """
        if self.head.next == self.tail:
            return ""
        return next(iter(self.head.next.keys))