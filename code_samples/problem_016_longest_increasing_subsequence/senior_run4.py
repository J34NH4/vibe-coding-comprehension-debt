from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Find the length of the longest strictly increasing subsequence.
        
        Uses binary search with patience sorting algorithm for O(n log n) complexity.
        
        Args:
            nums: List of integers to find LIS length from
            
        Returns:
            Length of the longest strictly increasing subsequence
            
        Raises:
            ValueError: If nums is empty
        """
        if not nums:
            raise ValueError("Input array cannot be empty")
            
        return self._binary_search_approach(nums)
    
    def _binary_search_approach(self, nums: List[int]) -> int:
        """
        Binary search approach using patience sorting algorithm.
        
        Args:
            nums: Input array of integers
            
        Returns:
            Length of longest increasing subsequence
        """
        tails_array = []  # tails[i] = smallest tail of all increasing subsequences of length i+1
        
        for current_number in nums:
            # Find leftmost position where current_number can be placed
            insertion_position = bisect.bisect_left(tails_array, current_number)
            
            if insertion_position == len(tails_array):
                # current_number is larger than all elements in tails_array
                tails_array.append(current_number)
            else:
                # Replace the element at insertion_position with current_number
                tails_array[insertion_position] = current_number
                
        return len(tails_array)
    
    def _dynamic_programming_approach(self, nums: List[int]) -> int:
        """
        Dynamic programming approach with O(n^2) complexity.
        
        Args:
            nums: Input array of integers
            
        Returns:
            Length of longest increasing subsequence
        """
        array_length = len(nums)
        dp_table = [1] * array_length  # dp_table[i] = length of LIS ending at index i
        
        for current_index in range(1, array_length):
            for previous_index in range(current_index):
                if nums[previous_index] < nums[current_index]:
                    # Can extend the subsequence ending at previous_index
                    dp_table[current_index] = max(
                        dp_table[current_index], 
                        dp_table[previous_index] + 1
                    )
        
        return max(dp_table)