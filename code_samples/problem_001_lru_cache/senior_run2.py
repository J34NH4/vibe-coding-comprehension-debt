from typing import Optional

class Node:
    """Doubly linked list node for LRU cache implementation."""
    
    def __init__(self, key: int = 0, value: int = 0) -> None:
        """Initialize a new node.
        
        Args:
            key: The key for this node
            value: The value for this node
        """
        self.key = key
        self.value = value
        self.previous: Optional[Node] = None
        self.next: Optional[Node] = None

class LRUCache:
    """Least Recently Used cache implementation using hashmap and doubly linked list."""

    def __init__(self, capacity: int) -> None:
        """Initialize LRU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Cache capacity must be at least 1")
            
        self.cache_capacity = capacity
        self.key_to_node = {}  # HashMap for O(1) lookup
        
        # Create dummy head and tail nodes for easier list manipulation
        self.head_sentinel = Node()
        self.tail_sentinel = Node()
        self.head_sentinel.next = self.tail_sentinel
        self.tail_sentinel.previous = self.head_sentinel

    def get(self, key: int) -> int:
        """Get value by key and mark as recently used.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or -1 if key doesn't exist
        """
        if key not in self.key_to_node:
            return -1
            
        target_node = self.key_to_node[key]
        self._move_to_head(target_node)  # Mark as most recently used
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
            self._move_to_head(existing_node)  # Mark as most recently used
        else:
            # Insert new key-value pair
            new_node = Node(key, value)
            
            if len(self.key_to_node) >= self.cache_capacity:
                # Remove least recently used item
                least_recently_used = self.tail_sentinel.previous
                self._remove_node(least_recently_used)
                del self.key_to_node[least_recently_used.key]
            
            self.key_to_node[key] = new_node
            self._add_to_head(new_node)  # Add as most recently used

    def _add_to_head(self, node: Node) -> None:
        """Add node right after head sentinel.
        
        Args:
            node: The node to add to the head of the list
        """
        node.previous = self.head_sentinel
        node.next = self.head_sentinel.next
        
        self.head_sentinel.next.previous = node
        self.head_sentinel.next = node

    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list.
        
        Args:
            node: The node to remove from the list
        """
        node.previous.next = node.next
        node.next.previous = node.previous

    def _move_to_head(self, node: Node) -> None:
        """Move existing node to head (mark as most recently used).
        
        Args:
            node: The node to move to the head of the list
        """
        self._remove_node(node)
        self._add_to_head(node)