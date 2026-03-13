from typing import Optional, Dict
from collections import defaultdict, OrderedDict


class LFUCache:
    """
    Implements a Least Frequently Used (LFU) cache with O(1) operations.
    
    When capacity is reached, removes the least frequently used key.
    Among keys with same frequency, removes the least recently used.
    """
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize the LFU cache with given capacity.
        
        Args:
            capacity: Maximum number of key-value pairs the cache can hold
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
            
        self.capacity: int = capacity
        self.minimum_frequency: int = 0
        
        # Maps key to value
        self.key_to_value: Dict[int, int] = {}
        
        # Maps key to its frequency
        self.key_to_frequency: Dict[int, int] = {}
        
        # Maps frequency to OrderedDict of keys (maintains insertion order for LRU within same frequency)
        self.frequency_to_keys: Dict[int, OrderedDict] = defaultdict(OrderedDict)
    
    def _update_frequency(self, key: int) -> None:
        """
        Update the frequency of a key and maintain frequency mappings.
        
        Args:
            key: The key whose frequency needs to be updated
        """
        current_frequency = self.key_to_frequency[key]
        new_frequency = current_frequency + 1
        
        # Remove key from current frequency bucket
        del self.frequency_to_keys[current_frequency][key]
        
        # If current frequency bucket is empty and it's the minimum, increment minimum
        if not self.frequency_to_keys[current_frequency] and current_frequency == self.minimum_frequency:
            self.minimum_frequency += 1
        
        # Add key to new frequency bucket
        self.key_to_frequency[key] = new_frequency
        self.frequency_to_keys[new_frequency][key] = True
    
    def _evict_least_frequent_key(self) -> None:
        """Remove the least frequently used key, breaking ties with LRU."""
        if not self.frequency_to_keys[self.minimum_frequency]:
            return
            
        # Get least recently used key among least frequent keys
        key_to_remove, _ = self.frequency_to_keys[self.minimum_frequency].popitem(last=False)
        
        # Clean up all mappings for the removed key
        del self.key_to_value[key_to_remove]
        del self.key_to_frequency[key_to_remove]
    
    def get(self, key: int) -> int:
        """
        Get the value associated with the key and update its frequency.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or -1 if key doesn't exist
        """
        if key not in self.key_to_value:
            return -1
        
        # Update frequency since key was accessed
        self._update_frequency(key)
        
        return self.key_to_value[key]
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if self.capacity == 0:
            return
        
        # Case 1: Key already exists - update value and frequency
        if key in self.key_to_value:
            self.key_to_value[key] = value
            self._update_frequency(key)
            return
        
        # Case 2: Cache is at capacity - evict least frequent key
        if len(self.key_to_value) >= self.capacity:
            self._evict_least_frequent_key()
        
        # Case 3: Insert new key with frequency 1
        self.key_to_value[key] = value
        self.key_to_frequency[key] = 1
        self.frequency_to_keys[1][key] = True
        self.minimum_frequency = 1  # New key always has frequency 1