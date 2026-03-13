from collections import defaultdict, OrderedDict
from typing import Optional, Any

class LFUCache:
    """
    Least Frequently Used (LFU) cache implementation.
    
    Maintains items based on frequency of access, removing least frequently
    used items when capacity is exceeded. For items with same frequency,
    uses LRU eviction policy.
    """
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize the LFU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
            
        self.capacity: int = capacity
        self.minimum_frequency: int = 1
        
        # Maps key to value
        self.key_to_value: dict[int, Any] = {}
        
        # Maps key to its frequency
        self.key_to_frequency: dict[int, int] = {}
        
        # Maps frequency to OrderedDict of keys (for LRU within same frequency)
        self.frequency_to_keys: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)

    def get(self, key: int) -> int:
        """
        Get value for the given key and update its frequency.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or -1 if key doesn't exist
        """
        if key not in self.key_to_value:
            return -1
            
        # Update frequency for accessed key
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
            
        if key in self.key_to_value:
            # Update existing key
            self.key_to_value[key] = value
            self._update_frequency(key)
        else:
            # Insert new key
            if len(self.key_to_value) >= self.capacity:
                self._evict_least_frequent()
                
            # Add new key with frequency 1
            self.key_to_value[key] = value
            self.key_to_frequency[key] = 1
            self.frequency_to_keys[1][key] = None
            self.minimum_frequency = 1

    def _update_frequency(self, key: int) -> None:
        """
        Update the frequency of a key and maintain data structure invariants.
        
        Args:
            key: The key whose frequency should be incremented
        """
        current_frequency = self.key_to_frequency[key]
        new_frequency = current_frequency + 1
        
        # Remove key from current frequency bucket
        del self.frequency_to_keys[current_frequency][key]
        
        # Update minimum frequency if needed
        if (self.minimum_frequency == current_frequency and 
            len(self.frequency_to_keys[current_frequency]) == 0):
            self.minimum_frequency += 1
            
        # Add key to new frequency bucket
        self.key_to_frequency[key] = new_frequency
        self.frequency_to_keys[new_frequency][key] = None

    def _evict_least_frequent(self) -> None:
        """
        Remove the least frequently used key from the cache.
        
        For keys with the same minimum frequency, removes the least recently used.
        """
        # Get the least recently used key with minimum frequency
        key_to_evict, _ = self.frequency_to_keys[self.minimum_frequency].popitem(last=False)
        
        # Clean up all references to the evicted key
        del self.key_to_value[key_to_evict]
        del self.key_to_frequency[key_to_evict]