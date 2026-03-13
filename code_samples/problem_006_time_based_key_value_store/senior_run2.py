from typing import Dict, List, Optional
from collections import defaultdict
import bisect

class TimeMap:
    """
    Time-based key-value store that supports storing multiple values for the same key
    at different timestamps and retrieving the value at or before a given timestamp.
    """
    
    def __init__(self) -> None:
        """Initialize the TimeMap data structure."""
        # Dictionary mapping key to list of (timestamp, value) tuples
        self.key_to_time_values: Dict[str, List[tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Stores the key with the given value at the specified timestamp.
        
        Args:
            key: The key to store
            value: The value to associate with the key
            timestamp: The timestamp when this key-value pair is valid
        """
        # Append to list - timestamps are guaranteed to be in increasing order
        self.key_to_time_values[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """
        Returns the value associated with key at or before the given timestamp.
        
        Args:
            key: The key to retrieve
            timestamp: The timestamp to query
            
        Returns:
            The value at or before the timestamp, or empty string if not found
        """
        if key not in self.key_to_time_values:
            return ""
        
        time_value_pairs = self.key_to_time_values[key]
        
        # Binary search for the rightmost timestamp <= given timestamp
        insertion_index = bisect.bisect_right(time_value_pairs, (timestamp, chr(127)))
        
        # If insertion_index is 0, no valid timestamp found
        if insertion_index == 0:
            return ""
        
        # Return the value at the largest valid timestamp
        return time_value_pairs[insertion_index - 1][1]