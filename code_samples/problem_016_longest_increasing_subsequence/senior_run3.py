from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Find the length of the longest strictly increasing subsequence.
        
        Uses binary search with a patience sorting approach for O(n log n) complexity.
        
        Args:
            nums: List of integers to find LIS length for
            
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
        Implements patience sorting algorithm using binary search.
        
        Maintains an array where tails[i] represents the smallest tail
        of all increasing subsequences of length i+1.
        
        Args:
            nums: Input array of integers
            
        Returns:
            Length of longest increasing subsequence
        """
        tails = []  # Store smallest tail for each subsequence length
        
        for current_number in nums:
            # Find leftmost position where current_number can be placed
            insertion_position = bisect.bisect_left(tails, current_number)
            
            if insertion_position == len(tails):
                # Current number extends the longest subsequence
                tails.append(current_number)
            else:
                # Replace existing tail with smaller value
                tails[insertion_position] = current_number
                
        return len(tails)
    
    def lengthOfLIS_dp(self, nums: List[int]) -> int:
        """
        Alternative dynamic programming solution with O(n²) complexity.
        
        Args:
            nums: List of integers
            
        Returns:
            Length of longest increasing subsequence
        """
        if not nums:
            return 0
            
        sequence_length = len(nums)
        # dp[i] represents length of LIS ending at index i
        dynamic_programming_table = [1] * sequence_length
        
        for current_index in range(1, sequence_length):
            for previous_index in range(current_index):
                if nums[previous_index] < nums[current_index]:
                    # Can extend subsequence ending at previous_index
                    dynamic_programming_table[current_index] = max(
                        dynamic_programming_table[current_index],
                        dynamic_programming_table[previous_index] + 1
                    )
        
        return max(dynamic_programming_table)