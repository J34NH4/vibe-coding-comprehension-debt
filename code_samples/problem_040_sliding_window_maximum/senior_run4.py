from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Find the maximum value in each sliding window of size k.
        
        Uses a monotonic decreasing deque to efficiently track potential
        maximums in O(n) time complexity.
        
        Args:
            nums: List of integers to process
            k: Size of the sliding window
            
        Returns:
            List of maximum values for each window position
            
        Raises:
            ValueError: If k is invalid or nums is empty
        """
        if not nums or k <= 0:
            raise ValueError("Invalid input: nums must be non-empty and k must be positive")
        
        if k > len(nums):
            raise ValueError("Window size cannot be larger than array length")
        
        # Special case: single element window
        if k == 1:
            return nums
        
        return self._sliding_window_maximum_deque(nums, k)
    
    def _sliding_window_maximum_deque(self, nums: List[int], window_size: int) -> List[int]:
        """
        Implementation using monotonic decreasing deque approach.
        
        Args:
            nums: Input array
            window_size: Size of sliding window
            
        Returns:
            List of maximum values for each window
        """
        # Deque stores indices, maintained in decreasing order of values
        index_deque = deque()
        result_maximums = []
        
        for current_index in range(len(nums)):
            current_value = nums[current_index]
            
            # Remove indices outside current window
            self._remove_outdated_indices(index_deque, current_index, window_size)
            
            # Maintain monotonic decreasing property
            self._maintain_decreasing_order(index_deque, nums, current_value)
            
            # Add current index
            index_deque.append(current_index)
            
            # Record maximum for complete windows
            if current_index >= window_size - 1:
                maximum_index = index_deque[0]  # Front has maximum value index
                result_maximums.append(nums[maximum_index])
        
        return result_maximums
    
    def _remove_outdated_indices(self, index_deque: deque, current_index: int, window_size: int) -> None:
        """
        Remove indices that are outside the current sliding window.
        
        Args:
            index_deque: Deque containing indices
            current_index: Current position in array
            window_size: Size of sliding window
        """
        while index_deque and index_deque[0] <= current_index - window_size:
            index_deque.popleft()
    
    def _maintain_decreasing_order(self, index_deque: deque, nums: List[int], current_value: int) -> None:
        """
        Remove indices from back while their values are smaller than current value.
        This maintains the monotonic decreasing property.
        
        Args:
            index_deque: Deque containing indices
            nums: Original array for value lookup
            current_value: Value at current position
        """
        while index_deque and nums[index_deque[-1]] < current_value:
            index_deque.pop()