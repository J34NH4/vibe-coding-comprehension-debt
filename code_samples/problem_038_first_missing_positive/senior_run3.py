class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        """
        Find the smallest missing positive integer in an unsorted array.
        
        Uses cyclic sort approach to achieve O(n) time and O(1) space complexity.
        The idea is to place each positive integer i at index i-1 if possible.
        
        Args:
            nums: List of integers (can contain negative numbers and zeros)
            
        Returns:
            The smallest missing positive integer
        """
        if not nums:
            return 1
            
        array_length = len(nums)
        
        # Place each positive integer at its correct position
        self._place_numbers_in_correct_positions(nums, array_length)
        
        # Find the first missing positive
        return self._find_first_missing_positive(nums, array_length)
    
    def _place_numbers_in_correct_positions(self, nums: list[int], array_length: int) -> None:
        """
        Place each number at its correct position using cyclic sort.
        
        For a number x, its correct position is index x-1 (if x is in range [1, n]).
        
        Args:
            nums: The array to modify in-place
            array_length: Length of the array
        """
        current_index = 0
        
        while current_index < array_length:
            target_number = nums[current_index]
            target_position = target_number - 1  # Position where this number should be
            
            # Check if number should be placed and is not already in correct position
            if (self._is_valid_positive_number(target_number, array_length) and 
                nums[target_position] != target_number):
                # Swap current number to its correct position
                nums[current_index], nums[target_position] = nums[target_position], nums[current_index]
            else:
                current_index += 1
    
    def _is_valid_positive_number(self, number: int, array_length: int) -> bool:
        """
        Check if a number is a valid positive integer within our range.
        
        Args:
            number: The number to check
            array_length: Maximum valid positive number (array length)
            
        Returns:
            True if number is in range [1, array_length], False otherwise
        """
        return 1 <= number <= array_length
    
    def _find_first_missing_positive(self, nums: list[int], array_length: int) -> int:
        """
        Find the first missing positive integer after sorting.
        
        Args:
            nums: Array where numbers are placed in their correct positions
            array_length: Length of the array
            
        Returns:
            The first missing positive integer
        """
        for expected_number in range(1, array_length + 1):
            array_index = expected_number - 1
            if nums[array_index] != expected_number:
                return expected_number
        
        # If all numbers 1 to n are present, return n+1
        return array_length + 1