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
            
        try:
            # Sort intervals by start time for efficient merging
            sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
        except (TypeError, IndexError) as e:
            raise ValueError("Invalid interval format") from e
            
        merged_intervals = []
        
        for current_interval in sorted_intervals:
            # If merged list is empty or current interval doesn't overlap with last merged
            if not merged_intervals or self._intervals_do_not_overlap(merged_intervals[-1], current_interval):
                merged_intervals.append(current_interval)
            else:
                # Merge overlapping intervals by extending the end time
                merged_intervals[-1] = self._merge_two_intervals(merged_intervals[-1], current_interval)
                
        return merged_intervals
    
    def _intervals_do_not_overlap(self, first_interval: List[int], second_interval: List[int]) -> bool:
        """
        Check if two intervals do not overlap.
        
        Args:
            first_interval: First interval [start, end]
            second_interval: Second interval [start, end]
            
        Returns:
            True if intervals do not overlap, False otherwise
        """
        return first_interval[1] < second_interval[0]
    
    def _merge_two_intervals(self, first_interval: List[int], second_interval: List[int]) -> List[int]:
        """
        Merge two overlapping intervals.
        
        Args:
            first_interval: First interval [start, end]
            second_interval: Second interval [start, end]
            
        Returns:
            Merged interval [min_start, max_end]
        """
        merged_start = min(first_interval[0], second_interval[0])
        merged_end = max(first_interval[1], second_interval[1])
        return [merged_start, merged_end]