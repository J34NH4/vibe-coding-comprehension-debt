from typing import Optional


class DoublyLinkedNode:
    """Represents a node in a doubly linked list for LRU cache implementation."""
    
    def __init__(self, key: int = 0, value: int = 0) -> None:
        """Initialize a doubly linked node.
        
        Args:
            key: The key associated with this node
            value: The value stored in this node
        """
        self.key = key
        self.value = value
        self.previous: Optional['DoublyLinkedNode'] = None
        self.next: Optional['DoublyLinkedNode'] = None


class LRUCache:
    """
    Least Recently Used (LRU) cache implementation using HashMap and Doubly Linked List.
    
    Provides O(1) time complexity for both get and put operations by maintaining
    a hash map for fast access and a doubly linked list for efficient insertion/deletion.
    """
    
    def __init__(self, capacity: int) -> None:
        """Initialize the LRU cache with given capacity.
        
        Args:
            capacity: Maximum number of key-value pairs the cache can hold
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Cache capacity must be at least 1")
            
        self.cache_capacity = capacity
        self.key_to_node = {}  # Hash map for O(1) access
        
        # Create dummy head and tail nodes to simplify edge cases
        self.dummy_head = DoublyLinkedNode()
        self.dummy_tail = DoublyLinkedNode()
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.previous = self.dummy_head

    def get(self, key: int) -> int:
        """Retrieve value by key and mark as recently used.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or -1 if key doesn't exist
        """
        if key not in self.key_to_node:
            return -1
            
        target_node = self.key_to_node[key]
        # Move accessed node to front (most recently used)
        self._move_node_to_front(target_node)
        return target_node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair in cache.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if key in self.key_to_node:
            # Update existing key
            existing_node = self.key_to_node[key]
            existing_node.value = value
            self._move_node_to_front(existing_node)
        else:
            # Insert new key-value pair
            new_node = DoublyLinkedNode(key, value)
            
            if len(self.key_to_node) >= self.cache_capacity:
                # Remove least recently used item
                self._remove_least_recently_used()
                
            self.key_to_node[key] = new_node
            self._add_node_to_front(new_node)

    def _add_node_to_front(self, node: DoublyLinkedNode) -> None:
        """Add node right after dummy head (most recently used position).
        
        Args:
            node: The node to add to the front
        """
        node.previous = self.dummy_head
        node.next = self.dummy_head.next
        
        self.dummy_head.next.previous = node
        self.dummy_head.next = node

    def _remove_node_from_list(self, node: DoublyLinkedNode) -> None:
        """Remove node from its current position in the doubly linked list.
        
        Args:
            node: The node to remove from the list
        """
        previous_node = node.previous
        next_node = node.next
        
        previous_node.next = next_node
        next_node.previous = previous_node

    def _move_node_to_front(self, node: DoublyLinkedNode) -> None:
        """Move existing node to front (mark as most recently used).
        
        Args:
            node: The node to move to the front
        """
        self._remove_node_from_list(node)
        self._add_node_to_front(node)

    def _remove_least_recently_used(self) -> None:
        """Remove the least recently used item from cache."""
        least_recently_used_node = self.dummy_tail.previous
        self._remove_node_from_list(least_recently_used_node)
        del self.key_to_node[least_recently_used_node.key]