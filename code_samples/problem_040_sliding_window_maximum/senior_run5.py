from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Find the maximum value in each sliding window of size k.
        
        Uses a monotonic deque to efficiently track potential maximums.
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
            raise ValueError("Invalid input parameters")
            
        result_maximums = []
        monotonic_deque = deque()  # Stores indices in decreasing order of values
        
        for current_index in range(len(nums)):
            current_value = nums[current_index]
            
            # Remove indices outside current window
            self._remove_outdated_indices(monotonic_deque, current_index, k)
            
            # Maintain decreasing order by removing smaller elements
            self._maintain_decreasing_order(monotonic_deque, nums, current_value)
            
            # Add current index to deque
            monotonic_deque.append(current_index)
            
            # If window is complete, record the maximum
            if current_index >= k - 1:
                maximum_index = monotonic_deque[0]
                result_maximums.append(nums[maximum_index])
                
        return result_maximums
    
    def _remove_outdated_indices(self, monotonic_deque: deque, current_index: int, window_size: int) -> None:
        """
        Remove indices that are outside the current sliding window.
        
        Args:
            monotonic_deque: Deque containing indices in decreasing order
            current_index: Current position in the array
            window_size: Size of the sliding window
        """
        while monotonic_deque and monotonic_deque[0] <= current_index - window_size:
            monotonic_deque.popleft()
    
    def _maintain_decreasing_order(self, monotonic_deque: deque, nums: List[int], current_value: int) -> None:
        """
        Remove elements from the back of deque that are smaller than current value.
        This maintains the decreasing order property of the deque.
        
        Args:
            monotonic_deque: Deque containing indices in decreasing order
            nums: Original array of numbers
            current_value: Value at current index
        """
        while monotonic_deque and nums[monotonic_deque[-1]] < current_value:
            monotonic_deque.pop()