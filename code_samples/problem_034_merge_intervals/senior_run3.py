from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Merge all overlapping intervals in the given array.
        
        Args:
            intervals: List of intervals where each interval is [start, end]
            
        Returns:
            List of merged intervals with no overlaps
            
        Raises:
            ValueError: If intervals contain invalid data
        """
        if not intervals:
            return []
        
        # Sort intervals by start time for efficient merging
        sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
        merged_intervals = []
        
        for current_interval in sorted_intervals:
            current_start, current_end = current_interval
            
            # First interval or no overlap with previous interval
            if not merged_intervals or merged_intervals[-1][1] < current_start:
                merged_intervals.append(current_interval)
            else:
                # Merge with previous interval by extending the end time
                previous_interval = merged_intervals[-1]
                previous_interval[1] = max(previous_interval[1], current_end)
        
        return merged_intervals