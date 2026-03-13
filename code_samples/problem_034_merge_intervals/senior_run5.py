from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Merges all overlapping intervals in the given array.
        
        Args:
            intervals: List of intervals where each interval is [start, end]
            
        Returns:
            List of merged intervals with no overlaps
            
        Raises:
            ValueError: If intervals contain invalid data
        """
        if not intervals:
            return []
        
        try:
            # Sort intervals by start time for efficient merging
            sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
        except (IndexError, TypeError) as error:
            raise ValueError(f"Invalid interval format: {error}")
        
        merged_intervals = []
        
        for current_interval in sorted_intervals:
            # If merged list is empty or no overlap with last interval
            if not merged_intervals or self._has_no_overlap(merged_intervals[-1], current_interval):
                merged_intervals.append(current_interval)
            else:
                # Merge with the last interval by extending the end time
                merged_intervals[-1] = self._merge_two_intervals(merged_intervals[-1], current_interval)
        
        return merged_intervals
    
    def _has_no_overlap(self, first_interval: List[int], second_interval: List[int]) -> bool:
        """
        Checks if two intervals have no overlap.
        
        Args:
            first_interval: First interval [start, end]
            second_interval: Second interval [start, end]
            
        Returns:
            True if intervals don't overlap, False otherwise
        """
        return first_interval[1] < second_interval[0]
    
    def _merge_two_intervals(self, first_interval: List[int], second_interval: List[int]) -> List[int]:
        """
        Merges two overlapping intervals into one.
        
        Args:
            first_interval: First interval [start, end]
            second_interval: Second interval [start, end]
            
        Returns:
            Merged interval spanning both input intervals
        """
        merged_start = min(first_interval[0], second_interval[0])
        merged_end = max(first_interval[1], second_interval[1])
        return [merged_start, merged_end]