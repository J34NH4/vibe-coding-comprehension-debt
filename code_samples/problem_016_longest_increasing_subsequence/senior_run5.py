from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Find the length of the longest strictly increasing subsequence.
        
        Uses binary search optimization with patience sorting approach.
        Time complexity: O(n log n), Space complexity: O(n)
        
        Args:
            nums: List of integers to find LIS in
            
        Returns:
            Length of longest increasing subsequence
            
        Raises:
            ValueError: If nums is empty
        """
        if not nums:
            raise ValueError("Input array cannot be empty")
            
        return self._binary_search_lis(nums)
    
    def _binary_search_lis(self, nums: List[int]) -> int:
        """
        Implementation using binary search for optimal time complexity.
        
        Maintains an array where tails[i] is the smallest tail element
        of all increasing subsequences of length i+1.
        
        Args:
            nums: Input array of integers
            
        Returns:
            Length of LIS
        """
        tails_array = []  # Store smallest tail for each subsequence length
        
        for current_number in nums:
            # Find leftmost position where current_number can be placed
            insertion_position = bisect.bisect_left(tails_array, current_number)
            
            if insertion_position == len(tails_array):
                # Current number extends the longest subsequence
                tails_array.append(current_number)
            else:
                # Replace existing element to maintain smallest tail property
                tails_array[insertion_position] = current_number
        
        return len(tails_array)
    
    def lengthOfLIS_dp(self, nums: List[int]) -> int:
        """
        Alternative dynamic programming solution for reference.
        
        Time complexity: O(n²), Space complexity: O(n)
        Less efficient but more intuitive approach.
        
        Args:
            nums: List of integers
            
        Returns:
            Length of longest increasing subsequence
        """
        if not nums:
            return 0
            
        sequence_length = len(nums)
        dp_table = [1] * sequence_length  # Each element forms subsequence of length 1
        
        for current_index in range(1, sequence_length):
            for previous_index in range(current_index):
                # If current element can extend subsequence ending at previous_index
                if nums[previous_index] < nums[current_index]:
                    dp_table[current_index] = max(
                        dp_table[current_index],
                        dp_table[previous_index] + 1
                    )
        
        return max(dp_table)