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
        
        # Phase 1: Place each positive integer in its correct position
        self._place_numbers_in_correct_positions(nums, array_length)
        
        # Phase 2: Find the first position where number doesn't match index + 1
        return self._find_first_missing_positive(nums, array_length)
    
    def _place_numbers_in_correct_positions(self, nums: List[int], array_length: int) -> None:
        """
        Place each number in its correct position using cyclic sort.
        
        For a positive integer x, it should be placed at index x-1.
        Only process numbers in range [1, array_length].
        
        Args:
            nums: The input array to modify in-place
            array_length: Length of the array
        """
        current_index = 0
        
        while current_index < array_length:
            current_number = nums[current_index]
            target_index = current_number - 1  # Where this number should be placed
            
            # Check if current number should be moved to a different position
            if (self._is_valid_positive_number(current_number, array_length) and 
                nums[target_index] != current_number):
                # Swap current number to its correct position
                nums[current_index], nums[target_index] = nums[target_index], nums[current_index]
            else:
                current_index += 1
    
    def _is_valid_positive_number(self, number: int, array_length: int) -> bool:
        """
        Check if a number is a valid positive integer that can be placed in the array.
        
        Args:
            number: The number to validate
            array_length: Maximum valid positive number (array length)
            
        Returns:
            True if number is in range [1, array_length], False otherwise
        """
        return 1 <= number <= array_length
    
    def _find_first_missing_positive(self, nums: List[int], array_length: int) -> int:
        """
        Find the first missing positive integer after numbers are sorted.
        
        Args:
            nums: Array with numbers placed in their correct positions
            array_length: Length of the array
            
        Returns:
            The smallest missing positive integer
        """
        # Check each position to see if it contains the expected number
        for position in range(array_length):
            expected_number = position + 1
            if nums[position] != expected_number:
                return expected_number
        
        # If all positions [1, array_length] are filled correctly
        return array_length + 1