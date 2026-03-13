from typing import Optional

class DoublyLinkedListNode:
    """Node for doubly linked list implementation."""
    
    def __init__(self, key: int = 0, value: int = 0) -> None:
        """Initialize a doubly linked list node.
        
        Args:
            key: The key for the cache entry
            value: The value for the cache entry
        """
        self.key = key
        self.value = value
        self.previous_node: Optional['DoublyLinkedListNode'] = None
        self.next_node: Optional['DoublyLinkedListNode'] = None

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
            raise ValueError("Capacity must be at least 1")
            
        self.cache_capacity = capacity
        self.key_to_node_map = {}  # Hash map for O(1) access
        
        # Create dummy head and tail nodes for easier list manipulation
        self.dummy_head = DoublyLinkedListNode()
        self.dummy_tail = DoublyLinkedListNode()
        self.dummy_head.next_node = self.dummy_tail
        self.dummy_tail.previous_node = self.dummy_head

    def get(self, key: int) -> int:
        """Get value by key and mark as most recently used.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or -1 if key doesn't exist
        """
        if key in self.key_to_node_map:
            target_node = self.key_to_node_map[key]
            self._move_to_head(target_node)  # Mark as most recently used
            return target_node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """Put key-value pair into cache.
        
        Args:
            key: The key to store
            value: The value to associate with the key
        """
        if key in self.key_to_node_map:
            # Update existing key
            existing_node = self.key_to_node_map[key]
            existing_node.value = value
            self._move_to_head(existing_node)  # Mark as most recently used
        else:
            # Add new key-value pair
            new_node = DoublyLinkedListNode(key, value)
            
            if len(self.key_to_node_map) >= self.cache_capacity:
                # Remove least recently used item
                least_recently_used_node = self.dummy_tail.previous_node
                self._remove_node(least_recently_used_node)
                del self.key_to_node_map[least_recently_used_node.key]
            
            # Add new node as most recently used
            self.key_to_node_map[key] = new_node
            self._add_to_head(new_node)

    def _add_to_head(self, target_node: DoublyLinkedListNode) -> None:
        """Add node right after dummy head.
        
        Args:
            target_node: Node to add to head position
        """
        target_node.previous_node = self.dummy_head
        target_node.next_node = self.dummy_head.next_node
        
        self.dummy_head.next_node.previous_node = target_node
        self.dummy_head.next_node = target_node

    def _remove_node(self, target_node: DoublyLinkedListNode) -> None:
        """Remove node from doubly linked list.
        
        Args:
            target_node: Node to remove from list
        """
        previous_node = target_node.previous_node
        next_node = target_node.next_node
        
        previous_node.next_node = next_node
        next_node.previous_node = previous_node

    def _move_to_head(self, target_node: DoublyLinkedListNode) -> None:
        """Move existing node to head position (mark as most recently used).
        
        Args:
            target_node: Node to move to head position
        """
        self._remove_node(target_node)
        self._add_to_head(target_node)