from typing import Dict, List, Optional
from collections import defaultdict
import bisect


class TimeMap:
    """
    A time-based key-value data structure that supports storing multiple values
    for the same key at different timestamps and retrieving the value at a
    specific timestamp or the most recent value before that timestamp.
    """
    
    def __init__(self) -> None:
        """
        Initialize the TimeMap data structure.
        
        Uses a dictionary where each key maps to a list of (timestamp, value) tuples
        stored in chronological order to enable binary search for efficient retrieval.
        """
        self.key_store: Dict[str, List[tuple[int, str]]] = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Store the key with the given value at the specified timestamp.
        
        Args:
            key: The key to store
            value: The value to associate with the key
            timestamp: The timestamp at which to store the key-value pair
            
        Note:
            Timestamps are guaranteed to be strictly increasing for each key,
            so we can simply append to maintain sorted order.
        """
        if not key:
            raise ValueError("Key cannot be empty")
        if timestamp < 0:
            raise ValueError("Timestamp must be non-negative")
            
        self.key_store[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Retrieve the value associated with the key at the given timestamp.
        
        If no value exists at the exact timestamp, returns the value with the
        largest timestamp that is less than or equal to the given timestamp.
        
        Args:
            key: The key to look up
            timestamp: The timestamp at which to retrieve the value
            
        Returns:
            The value at the specified timestamp, or the most recent value
            before that timestamp. Returns empty string if no such value exists.
        """
        if not key or key not in self.key_store:
            return ""
        
        if timestamp < 0:
            return ""
            
        timestamp_value_pairs = self.key_store[key]
        
        # Use binary search to find the rightmost timestamp <= given timestamp
        search_result = self._binary_search_timestamp(timestamp_value_pairs, timestamp)
        
        if search_result == -1:
            return ""  # No timestamp <= given timestamp exists
        
        return timestamp_value_pairs[search_result][1]  # Return the value
    
    def _binary_search_timestamp(self, timestamp_value_pairs: List[tuple[int, str]], 
                                target_timestamp: int) -> int:
        """
        Perform binary search to find the index of the largest timestamp
        that is less than or equal to the target timestamp.
        
        Args:
            timestamp_value_pairs: List of (timestamp, value) tuples in sorted order
            target_timestamp: The timestamp to search for
            
        Returns:
            Index of the element with the largest timestamp <= target_timestamp,
            or -1 if no such element exists.
        """
        if not timestamp_value_pairs:
            return -1
            
        left_index = 0
        right_index = len(timestamp_value_pairs) - 1
        result_index = -1
        
        while left_index <= right_index:
            middle_index = (left_index + right_index) // 2
            current_timestamp = timestamp_value_pairs[middle_index][0]
            
            if current_timestamp <= target_timestamp:
                result_index = middle_index  # Valid candidate
                left_index = middle_index + 1  # Look for a larger valid timestamp
            else:
                right_index = middle_index - 1  # Current timestamp too large
                
        return result_index