from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Find the maximum value in each sliding window of size k.
        
        Uses a monotonic deque to efficiently track potential maximums.
        Time complexity: O(n), Space complexity: O(k)
        
        Args:
            nums: Array of integers to process
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
            
        result_maximums: List[int] = []
        # Deque stores indices of array elements in decreasing order of their values
        monotonic_deque: deque = deque()
        
        # Process first window
        for window_index in range(k):
            self._add_element_to_deque(monotonic_deque, nums, window_index)
        
        # The front of deque contains index of maximum element
        result_maximums.append(nums[monotonic_deque[0]])
        
        # Process remaining elements
        for current_index in range(k, len(nums)):
            # Remove elements outside current window
            self._remove_elements_outside_window(monotonic_deque, current_index, k)
            
            # Add current element
            self._add_element_to_deque(monotonic_deque, nums, current_index)
            
            # Current maximum is at front of deque
            result_maximums.append(nums[monotonic_deque[0]])
        
        return result_maximums
    
    def _add_element_to_deque(self, monotonic_deque: deque, nums: List[int], current_index: int) -> None:
        """
        Add element at current_index to the monotonic deque.
        
        Removes all elements from back that are smaller than current element
        to maintain decreasing order.
        
        Args:
            monotonic_deque: Deque maintaining indices in decreasing order of values
            nums: Original array of numbers
            current_index: Index of element to add
        """
        # Remove elements smaller than current from back of deque
        while (monotonic_deque and 
               nums[monotonic_deque[-1]] <= nums[current_index]):
            monotonic_deque.pop()
        
        monotonic_deque.append(current_index)
    
    def _remove_elements_outside_window(self, monotonic_deque: deque, current_index: int, window_size: int) -> None:
        """
        Remove elements that are outside the current sliding window.
        
        Args:
            monotonic_deque: Deque containing indices
            current_index: Current position in the array
            window_size: Size of the sliding window
        """
        window_start_index = current_index - window_size + 1
        
        # Remove elements outside current window from front
        while (monotonic_deque and 
               monotonic_deque[0] < window_start_index):
            monotonic_deque.popleft()