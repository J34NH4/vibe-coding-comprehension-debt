from typing import Optional

class ListNode:
    """Node for doubly linked list implementation."""
    
    def __init__(self, key: int = 0, value: int = 0) -> None:
        """Initialize a list node with key and value.
        
        Args:
            key: The key for the cache entry
            value: The value for the cache entry
        """
        self.key = key
        self.value = value
        self.previous: Optional[ListNode] = None
        self.next: Optional[ListNode] = None

class LRUCache:
    """LRU Cache implementation using hashmap and doubly linked list."""
    
    def __init__(self, capacity: int) -> None:
        """Initialize LRU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Cache capacity must be at least 1")
            
        self.capacity = capacity
        self.cache_map = {}  # Maps key to node
        
        # Create dummy head and tail nodes for easier list manipulation
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.previous = self.head

    def get(self, key: int) -> int:
        """Get value for given key and mark as most recently used.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or -1 if key not found
        """
        if key not in self.cache_map:
            return -1
        
        node = self.cache_map[key]
        self._move_to_head(node)  # Mark as most recently used
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair in cache.
        
        Args:
            key: The key to insert/update
            value: The value to associate with the key
        """
        if key in self.cache_map:
            # Update existing key
            node = self.cache_map[key]
            node.value = value
            self._move_to_head(node)  # Mark as most recently used
        else:
            # Insert new key-value pair
            new_node = ListNode(key, value)
            
            if len(self.cache_map) >= self.capacity:
                # Remove least recently used item
                least_recent_node = self.tail.previous
                self._remove_node(least_recent_node)
                del self.cache_map[least_recent_node.key]
            
            self.cache_map[key] = new_node
            self._add_to_head(new_node)

    def _add_to_head(self, node: ListNode) -> None:
        """Add node right after head (most recently used position).
        
        Args:
            node: The node to add to head position
        """
        node.previous = self.head
        node.next = self.head.next
        
        self.head.next.previous = node
        self.head.next = node

    def _remove_node(self, node: ListNode) -> None:
        """Remove a node from the doubly linked list.
        
        Args:
            node: The node to remove from the list
        """
        previous_node = node.previous
        next_node = node.next
        
        previous_node.next = next_node
        next_node.previous = previous_node

    def _move_to_head(self, node: ListNode) -> None:
        """Move existing node to head (mark as most recently used).
        
        Args:
            node: The node to move to head position
        """
        self._remove_node(node)
        self._add_to_head(node)