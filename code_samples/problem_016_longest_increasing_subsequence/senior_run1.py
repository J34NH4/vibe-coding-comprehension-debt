from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Find the length of the longest strictly increasing subsequence.
        
        Uses binary search with patience sorting approach for O(n log n) complexity.
        
        Args:
            nums: List of integers to find LIS from
            
        Returns:
            Length of the longest increasing subsequence
            
        Raises:
            ValueError: If nums is empty
        """
        if not nums:
            raise ValueError("Input array cannot be empty")
            
        return self._binary_search_lis(nums)
    
    def _binary_search_lis(self, nums: List[int]) -> int:
        """
        Implementation using binary search and patience sorting.
        
        Args:
            nums: Input array of integers
            
        Returns:
            Length of LIS
        """
        tails = []  # tails[i] is the smallest tail of all increasing subsequences of length i+1
        
        for current_number in nums:
            insertion_position = self._find_insertion_position(tails, current_number)
            
            if insertion_position == len(tails):  # current_number is larger than all tails
                tails.append(current_number)
            else:  # Replace the tail at insertion_position
                tails[insertion_position] = current_number
                
        return len(tails)
    
    def _find_insertion_position(self, tails: List[int], target: int) -> int:
        """
        Find the leftmost position where target should be inserted to maintain sorted order.
        
        Args:
            tails: Sorted array of tail values
            target: Value to insert
            
        Returns:
            Index where target should be inserted
        """
        left_boundary = 0
        right_boundary = len(tails)
        
        while left_boundary < right_boundary:
            middle_index = (left_boundary + right_boundary) // 2
            
            if tails[middle_index] < target:
                left_boundary = middle_index + 1
            else:
                right_boundary = middle_index
                
        return left_boundary