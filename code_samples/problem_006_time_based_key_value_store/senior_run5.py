from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import bisect

class TimeMap:
    """
    A time-based key-value data structure that supports storing multiple values 
    for the same key at different timestamps and retrieving values based on timestamps.
    """
    
    def __init__(self) -> None:
        """
        Initialize the TimeMap data structure.
        Uses a dictionary where each key maps to a list of (timestamp, value) tuples
        maintained in sorted order by timestamp.
        """
        self.key_time_map: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Stores the key with the value at the given timestamp.
        
        Args:
            key: The key to store
            value: The value associated with the key
            timestamp: The timestamp for this key-value pair
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        # Append to list - timestamps are guaranteed to be in strictly increasing order
        self.key_time_map[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Retrieves a value such that set was called previously with timestamp_prev <= timestamp.
        If there are multiple such values, return the value with the largest timestamp_prev.
        If there are no values, return empty string.
        
        Args:
            key: The key to search for
            timestamp: The timestamp to query against
            
        Returns:
            The value associated with the largest timestamp <= given timestamp,
            or empty string if no such value exists
        """
        if not key or key not in self.key_time_map:
            return ""
        
        timestamp_value_pairs = self.key_time_map[key]
        
        if not timestamp_value_pairs:
            return ""
        
        # Find the rightmost timestamp that is <= given timestamp
        insertion_index = bisect.bisect_right(timestamp_value_pairs, (timestamp, chr(127)))
        
        # If insertion_index is 0, no timestamp is <= given timestamp
        if insertion_index == 0:
            return ""
        
        # Return the value at the largest valid timestamp
        return timestamp_value_pairs[insertion_index - 1][1]