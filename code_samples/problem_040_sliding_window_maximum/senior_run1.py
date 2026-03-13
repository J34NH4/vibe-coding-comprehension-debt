from collections import deque
from typing import List

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Find the maximum value in each sliding window of size k.
        
        Args:
            nums: List of integers to process
            k: Size of the sliding window
            
        Returns:
            List of maximum values for each window position
            
        Raises:
            ValueError: If k is invalid or nums is empty
        """
        if not nums or k <= 0 or k > len(nums):
            raise ValueError("Invalid input parameters")
            
        if k == 1:
            return nums
            
        # Deque stores indices of array elements in decreasing order of values
        window_deque = deque()
        result_maximums = []
        
        for current_index in range(len(nums)):
            # Remove indices that are out of current window
            self._remove_out_of_bounds_indices(window_deque, current_index, k)
            
            # Remove indices whose corresponding values are smaller than current
            self._remove_smaller_elements(window_deque, nums, current_index)
            
            # Add current element index
            window_deque.append(current_index)
            
            # The front of deque contains index of maximum element in current window
            if current_index >= k - 1:  # Window is complete
                maximum_value = nums[window_deque[0]]
                result_maximums.append(maximum_value)
                
        return result_maximums
    
    def _remove_out_of_bounds_indices(self, window_deque: deque, current_index: int, window_size: int) -> None:
        """
        Remove indices that are outside the current sliding window.
        
        Args:
            window_deque: Deque containing indices
            current_index: Current position in the array
            window_size: Size of the sliding window
        """
        while window_deque and window_deque[0] <= current_index - window_size:
            window_deque.popleft()
    
    def _remove_smaller_elements(self, window_deque: deque, nums: List[int], current_index: int) -> None:
        """
        Remove indices whose values are smaller than the current element.
        
        Args:
            window_deque: Deque containing indices
            nums: Original array of numbers
            current_index: Current position in the array
        """
        current_value = nums[current_index]
        while window_deque and nums[window_deque[-1]] < current_value:
            window_deque.pop()