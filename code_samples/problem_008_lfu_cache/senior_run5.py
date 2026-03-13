from collections import defaultdict, OrderedDict
from typing import Optional


class LFUCache:
    """
    Least Frequently Used (LFU) Cache implementation.
    
    Maintains cache with capacity limit, evicting least frequently used items.
    On tie in frequency, evicts least recently used item.
    """
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize LFU cache with given capacity.
        
        Args:
            capacity: Maximum number of items cache can hold
        """
        self.capacity = capacity
        self.min_frequency = 0
        self.key_to_value = {}  # key -> value mapping
        self.key_to_frequency = {}  # key -> frequency mapping
        self.frequency_to_keys = defaultdict(OrderedDict)  # frequency -> ordered keys
    
    def get(self, key: int) -> int:
        """
        Get value for given key and update frequency.
        
        Args:
            key: Key to retrieve value for
            
        Returns:
            Value associated with key, or -1 if key doesn't exist
        """
        if key not in self.key_to_value:
            return -1
        
        # Update frequency for accessed key
        self._update_frequency(key)
        return self.key_to_value[key]
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update key-value pair in cache.
        
        Args:
            key: Key to insert/update
            value: Value to associate with key
        """
        if self.capacity <= 0:
            return
        
        if key in self.key_to_value:
            # Update existing key
            self.key_to_value[key] = value
            self._update_frequency(key)
            return
        
        # Handle capacity limit for new key
        if len(self.key_to_value) >= self.capacity:
            self._evict_lfu_key()
        
        # Insert new key-value pair
        self.key_to_value[key] = value
        self.key_to_frequency[key] = 1
        self.frequency_to_keys[1][key] = None  # Use OrderedDict as ordered set
        self.min_frequency = 1
    
    def _update_frequency(self, key: int) -> None:
        """
        Update frequency count for given key.
        
        Args:
            key: Key to update frequency for
        """
        current_frequency = self.key_to_frequency[key]
        new_frequency = current_frequency + 1
        
        # Remove key from current frequency bucket
        del self.frequency_to_keys[current_frequency][key]
        
        # Update min_frequency if current bucket becomes empty
        if not self.frequency_to_keys[current_frequency] and current_frequency == self.min_frequency:
            self.min_frequency += 1
        
        # Add key to new frequency bucket
        self.key_to_frequency[key] = new_frequency
        self.frequency_to_keys[new_frequency][key] = None
    
    def _evict_lfu_key(self) -> None:
        """
        Evict least frequently used key from cache.
        On frequency tie, evicts least recently used key.
        """
        if not self.frequency_to_keys[self.min_frequency]:
            return
        
        # Get least recently used key from min frequency bucket
        lfu_key, _ = self.frequency_to_keys[self.min_frequency].popitem(last=False)
        
        # Remove key from all tracking dictionaries
        del self.key_to_value[lfu_key]
        del self.key_to_frequency[lfu_key]