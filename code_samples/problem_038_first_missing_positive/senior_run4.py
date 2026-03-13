from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        """
        Find the first missing positive integer in an unsorted array.
        
        Uses cyclic sort approach to achieve O(n) time and O(1) space complexity.
        The idea is to place each positive integer i at index i-1 if possible.
        
        Args:
            nums: List of integers (can contain negative numbers and duplicates)
            
        Returns:
            The smallest missing positive integer
            
        Raises:
            None
        """
        if not nums:
            return 1
            
        array_length = len(nums)
        
        # First pass: place each positive integer at its correct position
        self._place_numbers_at_correct_positions(nums, array_length)
        
        # Second pass: find the first position where number doesn't match index + 1
        return self._find_first_missing_positive(nums, array_length)
    
    def _place_numbers_at_correct_positions(self, nums: List[int], array_length: int) -> None:
        """
        Place each positive integer i at index i-1 using cyclic sort.
        
        Args:
            nums: The array to modify in-place
            array_length: Length of the array
        """
        current_index = 0
        
        while current_index < array_length:
            current_value = nums[current_index]
            target_index = current_value - 1  # Where this number should be placed
            
            # Check if current number should be moved to a different position
            if self._should_move_number(current_value, target_index, array_length, nums):
                # Swap current number to its correct position
                nums[current_index], nums[target_index] = nums[target_index], nums[current_index]
            else:
                current_index += 1
    
    def _should_move_number(self, current_value: int, target_index: int, 
                           array_length: int, nums: List[int]) -> bool:
        """
        Determine if a number should be moved to its target position.
        
        Args:
            current_value: The number to check
            target_index: Where the number should be placed
            array_length: Length of the array
            nums: The array being processed
            
        Returns:
            True if the number should be moved, False otherwise
        """
        # Number is positive and within valid range
        is_valid_positive = 1 <= current_value <= array_length
        # Target position is valid
        is_valid_target = 0 <= target_index < array_length
        # Target position doesn't already have the correct number
        target_position_incorrect = nums[target_index] != current_value
        
        return is_valid_positive and is_valid_target and target_position_incorrect
    
    def _find_first_missing_positive(self, nums: List[int], array_length: int) -> int:
        """
        Find the first missing positive integer after placement.
        
        Args:
            nums: Array with numbers placed at correct positions
            array_length: Length of the array
            
        Returns:
            The first missing positive integer
        """
        for position_index in range(array_length):
            expected_value = position_index + 1
            actual_value = nums[position_index]
            
            if actual_value != expected_value:  # Found first missing positive
                return expected_value
        
        # All positions 1 to n are filled correctly
        return array_length + 1