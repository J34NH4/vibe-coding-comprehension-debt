from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Find the maximum value in each sliding window of size k.
        
        Uses a monotonic decreasing deque to efficiently track potential maximums.
        The deque stores indices of elements in decreasing order of their values.
        
        Args:
            nums: List of integers to process
            k: Size of the sliding window
            
        Returns:
            List of maximum values for each window position
            
        Raises:
            ValueError: If k is invalid or nums is empty
        """
        if not nums or k <= 0 or k > len(nums):
            raise ValueError("Invalid input: nums cannot be empty and k must be valid")
            
        maximum_values = []
        window_deque = deque()  # Stores indices in decreasing order of values
        
        for current_index in range(len(nums)):
            current_value = nums[current_index]
            
            # Remove indices that are outside current window
            self._remove_outdated_indices(window_deque, current_index, k)
            
            # Remove indices whose values are smaller than current value
            self._maintain_decreasing_order(window_deque, nums, current_value)
            
            # Add current index to deque
            window_deque.append(current_index)
            
            # If we have processed at least k elements, record the maximum
            if current_index >= k - 1:
                maximum_index = window_deque[0]  # Front has the maximum value index
                maximum_values.append(nums[maximum_index])
                
        return maximum_values
    
    def _remove_outdated_indices(self, window_deque: deque, current_index: int, window_size: int) -> None:
        """
        Remove indices from deque that are outside the current window.
        
        Args:
            window_deque: Deque containing indices
            current_index: Current position in the array
            window_size: Size of the sliding window
        """
        while window_deque and window_deque[0] <= current_index - window_size:
            window_deque.popleft()
    
    def _maintain_decreasing_order(self, window_deque: deque, nums: List[int], current_value: int) -> None:
        """
        Remove indices from the back of deque whose values are smaller than current value.
        This maintains the decreasing order property of the deque.
        
        Args:
            window_deque: Deque containing indices
            nums: Original array of numbers
            current_value: Value at current index
        """
        while window_deque and nums[window_deque[-1]] < current_value:
            window_deque.pop()