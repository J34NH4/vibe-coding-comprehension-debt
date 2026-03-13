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
            
        # Validate input intervals
        self._validate_intervals(intervals)
        
        # Sort intervals by start time for efficient merging
        sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
        
        merged_intervals = []
        current_interval = sorted_intervals[0]
        
        for next_interval in sorted_intervals[1:]:
            if self._intervals_overlap(current_interval, next_interval):
                # Merge overlapping intervals
                current_interval = self._merge_two_intervals(current_interval, next_interval)
            else:
                # No overlap, add current interval to result and move to next
                merged_intervals.append(current_interval)
                current_interval = next_interval
        
        # Add the final interval
        merged_intervals.append(current_interval)
        
        return merged_intervals
    
    def _validate_intervals(self, intervals: List[List[int]]) -> None:
        """
        Validates that all intervals are properly formatted.
        
        Args:
            intervals: List of intervals to validate
            
        Raises:
            ValueError: If any interval is invalid
        """
        for interval in intervals:
            if len(interval) != 2:
                raise ValueError(f"Invalid interval format: {interval}")
            if interval[0] > interval[1]:
                raise ValueError(f"Invalid interval: start > end: {interval}")
    
    def _intervals_overlap(self, interval_a: List[int], interval_b: List[int]) -> bool:
        """
        Checks if two intervals overlap or are adjacent.
        
        Args:
            interval_a: First interval [start, end]
            interval_b: Second interval [start, end]
            
        Returns:
            True if intervals overlap, False otherwise
        """
        return interval_a[1] >= interval_b[0]
    
    def _merge_two_intervals(self, interval_a: List[int], interval_b: List[int]) -> List[int]:
        """
        Merges two overlapping intervals into one.
        
        Args:
            interval_a: First interval [start, end]
            interval_b: Second interval [start, end]
            
        Returns:
            Merged interval [min_start, max_end]
        """
        merged_start = min(interval_a[0], interval_b[0])
        merged_end = max(interval_a[1], interval_b[1])
        return [merged_start, merged_end]