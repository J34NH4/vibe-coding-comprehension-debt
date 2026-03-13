from typing import Optional

class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation using doubly linked list and hash map.
    
    Provides O(1) time complexity for both get and put operations by maintaining
    a doubly linked list for ordering and a hash map for fast key lookup.
    """
    
    class _DoublyLinkedNode:
        """
        Internal node class for the doubly linked list.
        
        Each node contains a key-value pair and pointers to previous and next nodes.
        """
        
        def __init__(self, key: int = 0, value: int = 0) -> None:
            """
            Initialize a doubly linked node.
            
            Args:
                key: The cache key
                value: The cache value
            """
            self.key: int = key
            self.value: int = value
            self.previous: Optional['LRUCache._DoublyLinkedNode'] = None
            self.next: Optional['LRUCache._DoublyLinkedNode'] = None

    def __init__(self, capacity: int) -> None:
        """
        Initialize the LRU Cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is less than or equal to 0
        """
        if capacity <= 0:
            raise ValueError("Cache capacity must be positive")
            
        self.cache_capacity: int = capacity
        self.key_to_node: dict[int, LRUCache._DoublyLinkedNode] = {}
        
        # Create dummy head and tail nodes to simplify edge cases
        self.head_sentinel: LRUCache._DoublyLinkedNode = self._DoublyLinkedNode()
        self.tail_sentinel: LRUCache._DoublyLinkedNode = self._DoublyLinkedNode()
        self.head_sentinel.next = self.tail_sentinel
        self.tail_sentinel.previous = self.head_sentinel

    def get(self, key: int) -> int:
        """
        Retrieve value by key from the cache.
        
        If key exists, moves the corresponding node to the front (most recently used).
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or -1 if key doesn't exist
        """
        if key in self.key_to_node:
            target_node = self.key_to_node[key]
            self._move_node_to_front(target_node)  # Mark as recently used
            return target_node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        
        If key exists, updates the value and moves to front.
        If key doesn't exist, adds new node. If capacity exceeded, removes LRU item.
        
        Args:
            key: The key to insert/update
            value: The value to associate with the key
        """
        if key in self.key_to_node:
            # Update existing key
            existing_node = self.key_to_node[key]
            existing_node.value = value
            self._move_node_to_front(existing_node)  # Mark as recently used
        else:
            # Add new key-value pair
            new_node = self._DoublyLinkedNode(key, value)
            self.key_to_node[key] = new_node
            self._add_node_to_front(new_node)
            
            # Remove least recently used item if capacity exceeded
            if len(self.key_to_node) > self.cache_capacity:
                self._remove_least_recently_used()

    def _add_node_to_front(self, node: _DoublyLinkedNode) -> None:
        """
        Add a node right after the head sentinel (most recently used position).
        
        Args:
            node: The node to add to the front
        """
        node.previous = self.head_sentinel
        node.next = self.head_sentinel.next
        
        self.head_sentinel.next.previous = node
        self.head_sentinel.next = node

    def _remove_node_from_list(self, node: _DoublyLinkedNode) -> None:
        """
        Remove a node from the doubly linked list.
        
        Args:
            node: The node to remove from the list
        """
        node.previous.next = node.next
        node.next.previous = node.previous

    def _move_node_to_front(self, node: _DoublyLinkedNode) -> None:
        """
        Move an existing node to the front (most recently used position).
        
        Args:
            node: The node to move to the front
        """
        self._remove_node_from_list(node)
        self._add_node_to_front(node)

    def _remove_least_recently_used(self) -> None:
        """
        Remove the least recently used item (node before tail sentinel).
        
        Updates both the linked list and the hash map.
        """
        lru_node = self.tail_sentinel.previous
        self._remove_node_from_list(lru_node)
        del self.key_to_node[lru_node.key]  # Remove from hash map