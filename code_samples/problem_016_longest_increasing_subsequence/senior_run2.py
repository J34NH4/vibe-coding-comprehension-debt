from typing import List
import bisect

class Solution:
    """Solution for finding the longest increasing subsequence."""
    
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Find the length of the longest strictly increasing subsequence.
        
        Uses binary search with patience sorting algorithm for O(n log n) complexity.
        
        Args:
            nums: List of integers to find LIS from
            
        Returns:
            Length of the longest increasing subsequence
            
        Raises:
            ValueError: If nums is empty
        """
        if not nums:
            raise ValueError("Input array cannot be empty")
            
        return self._binary_search_approach(nums)
    
    def _binary_search_approach(self, nums: List[int]) -> int:
        """
        Binary search approach using patience sorting.
        
        Maintains an array where tails[i] is the smallest tail of all 
        increasing subsequences of length i+1.
        
        Args:
            nums: Input array of integers
            
        Returns:
            Length of longest increasing subsequence
        """
        tails_array = []  # Stores smallest tail for each subsequence length
        
        for current_number in nums:
            # Find leftmost position where current_number can be placed
            insertion_position = bisect.bisect_left(tails_array, current_number)
            
            if insertion_position == len(tails_array):
                # Current number is larger than all tails - extend sequence
                tails_array.append(current_number)
            else:
                # Replace existing tail with smaller value for same length
                tails_array[insertion_position] = current_number
                
        return len(tails_array)
    
    def lengthOfLIS_dp(self, nums: List[int]) -> int:
        """
        Dynamic programming approach for LIS (O(n^2) complexity).
        
        Alternative implementation using bottom-up DP.
        
        Args:
            nums: List of integers to find LIS from
            
        Returns:
            Length of the longest increasing subsequence
        """
        if not nums:
            return 0
            
        sequence_length = len(nums)
        dp_lengths = [1] * sequence_length  # Each element forms subsequence of length 1
        
        for current_index in range(1, sequence_length):
            for previous_index in range(current_index):
                # If current element is greater, we can extend the subsequence
                if nums[current_index] > nums[previous_index]:
                    dp_lengths[current_index] = max(
                        dp_lengths[current_index],
                        dp_lengths[previous_index] + 1
                    )
        
        return max(dp_lengths)