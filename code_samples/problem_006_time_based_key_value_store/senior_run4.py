from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import bisect

class TimeMap:
    """
    A time-based key-value data structure that supports storing multiple values
    for the same key at different timestamps and retrieving the most recent value
    for a given key at or before a specific timestamp.
    """
    
    def __init__(self) -> None:
        """
        Initialize the TimeMap data structure.
        """
        # Dictionary mapping keys to list of (timestamp, value) tuples
        self._data: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Stores the key with the value at the given time timestamp.
        
        Args:
            key: The key to store
            value: The value associated with the key
            timestamp: The timestamp when this key-value pair is set
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("Key and value must be strings")
        if not isinstance(timestamp, int) or timestamp < 1:
            raise ValueError("Timestamp must be a positive integer")
            
        # Append to maintain chronological order (timestamps are strictly increasing)
        self._data[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Returns a value such that set was called previously, with timestamp_prev <= timestamp.
        If there are multiple such values, it returns the value associated with the largest timestamp_prev.
        If there are no values, it returns an empty string.
        
        Args:
            key: The key to retrieve
            timestamp: The timestamp to query for
            
        Returns:
            The value associated with the largest timestamp <= given timestamp,
            or empty string if no such value exists
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not isinstance(timestamp, int) or timestamp < 1:
            raise ValueError("Timestamp must be a positive integer")
            
        if key not in self._data:
            return ""
        
        timestamp_value_pairs = self._data[key]
        
        # Binary search for the rightmost timestamp <= given timestamp
        insertion_index = bisect.bisect_right(timestamp_value_pairs, (timestamp, chr(127)))
        
        # If insertion_index is 0, no timestamp <= given timestamp exists
        if insertion_index == 0:
            return ""
        
        # Return the value at the largest valid timestamp
        return timestamp_value_pairs[insertion_index - 1][1]