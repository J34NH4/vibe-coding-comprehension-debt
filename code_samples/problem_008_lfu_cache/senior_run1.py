from typing import Dict, Optional
from collections import defaultdict, OrderedDict


class Node:
    """Represents a node in the LFU cache containing key-value pair and frequency."""
    
    def __init__(self, key: int, value: int) -> None:
        """Initialize a cache node.
        
        Args:
            key: The cache key
            value: The cache value
        """
        self.key = key
        self.value = value
        self.frequency = 1


class LFUCache:
    """Least Frequently Used cache implementation with O(1) operations."""
    
    def __init__(self, capacity: int) -> None:
        """Initialize the LFU cache.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.minimum_frequency = 0
        self.key_to_node: Dict[int, Node] = {}
        self.frequency_to_keys: Dict[int, OrderedDict] = defaultdict(OrderedDict)
    
    def _update_frequency(self, node: Node) -> None:
        """Update the frequency of a node and maintain frequency mappings.
        
        Args:
            node: The node whose frequency needs to be updated
        """
        old_frequency = node.frequency
        new_frequency = old_frequency + 1
        
        # Remove from old frequency group
        del self.frequency_to_keys[old_frequency][node.key]
        
        # Update minimum frequency if needed
        if old_frequency == self.minimum_frequency and not self.frequency_to_keys[old_frequency]:
            self.minimum_frequency += 1
        
        # Add to new frequency group
        node.frequency = new_frequency
        self.frequency_to_keys[new_frequency][node.key] = node
    
    def _evict_least_frequent(self) -> None:
        """Remove the least frequently used item from the cache."""
        if not self.frequency_to_keys[self.minimum_frequency]:
            return
        
        # Get least recently used item among least frequent items
        evicted_key, evicted_node = self.frequency_to_keys[self.minimum_frequency].popitem(last=False)
        del self.key_to_node[evicted_key]
    
    def get(self, key: int) -> int:
        """Retrieve value from cache and update its frequency.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or -1 if not found
        """
        if key not in self.key_to_node:
            return -1
        
        node = self.key_to_node[key]
        self._update_frequency(node)  # Increment usage frequency
        
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """Insert or update a key-value pair in the cache.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if self.capacity <= 0:
            return
        
        if key in self.key_to_node:
            # Update existing key
            existing_node = self.key_to_node[key]
            existing_node.value = value
            self._update_frequency(existing_node)
        else:
            # Insert new key
            if len(self.key_to_node) >= self.capacity:
                self._evict_least_frequent()
            
            new_node = Node(key, value)
            self.key_to_node[key] = new_node
            self.frequency_to_keys[1][key] = new_node  # New items start with frequency 1
            self.minimum_frequency = 1  # Reset minimum frequency for new item