from collections import defaultdict, OrderedDict
from typing import Optional, Dict


class LFUCache:
    """
    Least Frequently Used (LFU) cache implementation.
    
    When the cache reaches its capacity, it should invalidate and remove the least
    frequently used item before inserting a new item. For the purpose of this problem,
    when there is a tie (i.e., two or more keys with the same frequency), the least
    recently used key would be invalidated.
    """
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize the LFU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.minimum_frequency = 0  # Track minimum frequency for eviction
        
        # Maps key to [value, frequency]
        self.key_to_value_frequency: Dict[int, list] = {}
        
        # Maps frequency to OrderedDict of keys (for LRU within same frequency)
        self.frequency_to_keys: Dict[int, OrderedDict] = defaultdict(OrderedDict)

    def get(self, key: int) -> int:
        """
        Get the value of the key if the key exists in the cache.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or -1 if key doesn't exist
        """
        if key not in self.key_to_value_frequency:
            return -1
        
        # Update frequency for accessed key
        self._update_frequency(key)
        
        return self.key_to_value_frequency[key][0]  # Return value

    def put(self, key: int, value: int) -> None:
        """
        Update the value of the key if present, or inserts the key if not already present.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if self.capacity <= 0:
            return
        
        if key in self.key_to_value_frequency:
            # Update existing key
            self.key_to_value_frequency[key][0] = value
            self._update_frequency(key)
            return
        
        # Need to add new key
        if len(self.key_to_value_frequency) >= self.capacity:
            self._evict_least_frequent_key()
        
        # Insert new key with frequency 1
        self.key_to_value_frequency[key] = [value, 1]
        self.frequency_to_keys[1][key] = None  # Add to frequency 1 group
        self.minimum_frequency = 1  # New key always has frequency 1

    def _update_frequency(self, key: int) -> None:
        """
        Update the frequency of a key and maintain frequency groups.
        
        Args:
            key: The key whose frequency should be incremented
        """
        value, current_frequency = self.key_to_value_frequency[key]
        new_frequency = current_frequency + 1
        
        # Update key's frequency
        self.key_to_value_frequency[key][1] = new_frequency
        
        # Remove from current frequency group
        del self.frequency_to_keys[current_frequency][key]
        
        # Add to new frequency group
        self.frequency_to_keys[new_frequency][key] = None
        
        # Update minimum frequency if necessary
        if (current_frequency == self.minimum_frequency and 
            not self.frequency_to_keys[current_frequency]):
            self.minimum_frequency += 1

    def _evict_least_frequent_key(self) -> None:
        """
        Evict the least frequently used key (LRU among ties).
        """
        # Get the least recently used key from minimum frequency group
        key_to_evict, _ = self.frequency_to_keys[self.minimum_frequency].popitem(last=False)
        
        # Remove from main storage
        del self.key_to_value_frequency[key_to_evict]