from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        """
        Find the smallest missing positive integer in an unsorted array.
        
        Uses cyclic sort approach to achieve O(n) time and O(1) space complexity.
        The idea is to place each positive integer i at index i-1 if possible.
        
        Args:
            nums: List of integers (can be negative, zero, or positive)
            
        Returns:
            The smallest missing positive integer (starting from 1)
        """
        if not nums:
            return 1
            
        array_length = len(nums)
        
        # Phase 1: Place each positive integer at its correct position
        self._place_numbers_at_correct_positions(nums, array_length)
        
        # Phase 2: Find the first missing positive
        return self._find_first_missing_positive(nums, array_length)
    
    def _place_numbers_at_correct_positions(self, nums: List[int], array_length: int) -> None:
        """
        Place each number at its correct position using cyclic sort.
        
        For a number x, its correct position is index x-1 (if x is in range [1, n]).
        
        Args:
            nums: The array to modify in-place
            array_length: Length of the array
        """
        current_index = 0
        
        while current_index < array_length:
            current_number = nums[current_index]
            target_index = current_number - 1  # Where this number should be placed
            
            # Check if number should be placed and isn't already in correct position
            if (self._is_valid_positive_number(current_number, array_length) and 
                nums[target_index] != current_number):
                # Swap current number to its correct position
                nums[current_index], nums[target_index] = nums[target_index], nums[current_index]
            else:
                current_index += 1
    
    def _is_valid_positive_number(self, number: int, array_length: int) -> bool:
        """
        Check if a number is a valid positive integer within our range.
        
        Args:
            number: The number to validate
            array_length: Maximum valid positive number (array length)
            
        Returns:
            True if number is positive and within range [1, array_length]
        """
        return 1 <= number <= array_length
    
    def _find_first_missing_positive(self, nums: List[int], array_length: int) -> int:
        """
        Find the first missing positive integer after sorting.
        
        Args:
            nums: Array where numbers should be at correct positions
            array_length: Length of the array
            
        Returns:
            The smallest missing positive integer
        """
        # Check each position to see if correct number is present
        for expected_number in range(1, array_length + 1):
            position_index = expected_number - 1
            
            if nums[position_index] != expected_number:
                return expected_number
        
        # All numbers from 1 to n are present, return n+1
        return array_length + 1