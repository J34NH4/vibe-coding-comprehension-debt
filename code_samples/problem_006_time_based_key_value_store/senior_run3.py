from typing import Dict, List, Optional
from collections import defaultdict
import bisect

class TimeMap:
    """
    A time-based key-value data structure that stores multiple values 
    for the same key at different timestamps and supports efficient retrieval.
    """
    
    def __init__(self) -> None:
        """
        Initialize the TimeMap data structure.
        Uses a dictionary where each key maps to a list of (timestamp, value) tuples.
        """
        # Dictionary mapping keys to lists of (timestamp, value) tuples
        self.key_to_timestamp_values: Dict[str, List[tuple]] = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Stores the key with the given value at the specified timestamp.
        
        Args:
            key: The key to store
            value: The value associated with the key
            timestamp: The timestamp when this key-value pair is valid
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Key and value must be strings")
        
        if timestamp < 0:
            raise ValueError("Timestamp must be non-negative")
        
        # Append to the list for this key - timestamps are guaranteed to be in increasing order
        self.key_to_timestamp_values[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Returns the value associated with key at the largest timestamp 
        that is less than or equal to the given timestamp.
        
        Args:
            key: The key to retrieve
            timestamp: The timestamp to query
            
        Returns:
            The value at the largest timestamp <= given timestamp, or empty string if not found
        """
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        
        if timestamp < 0:
            raise ValueError("Timestamp must be non-negative")
        
        # Get the list of (timestamp, value) tuples for this key
        timestamp_value_pairs = self.key_to_timestamp_values.get(key, [])
        
        if not timestamp_value_pairs:
            return ""
        
        # Find the rightmost timestamp that is <= given timestamp
        target_index = self._find_largest_timestamp_index(timestamp_value_pairs, timestamp)
        
        if target_index == -1:
            return ""  # No timestamp <= given timestamp found
        
        return timestamp_value_pairs[target_index][1]  # Return the value
    
    def _find_largest_timestamp_index(self, timestamp_value_pairs: List[tuple], target_timestamp: int) -> int:
        """
        Find the index of the largest timestamp that is <= target_timestamp.
        
        Args:
            timestamp_value_pairs: List of (timestamp, value) tuples sorted by timestamp
            target_timestamp: The timestamp to search for
            
        Returns:
            Index of the largest timestamp <= target_timestamp, or -1 if none found
        """
        if not timestamp_value_pairs:
            return -1
        
        # Extract just the timestamps for binary search
        timestamps = [pair[0] for pair in timestamp_value_pairs]
        
        # Use bisect_right to find insertion point, then subtract 1 to get largest <= element
        insertion_index = bisect.bisect_right(timestamps, target_timestamp)
        
        # If insertion_index is 0, no timestamp <= target_timestamp exists
        if insertion_index == 0:
            return -1
        
        return insertion_index - 1