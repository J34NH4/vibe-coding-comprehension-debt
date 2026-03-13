class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        """
        Find the first missing positive integer in an unsorted array.
        
        Args:
            nums: List of integers that may contain negatives, zeros, and positives
            
        Returns:
            The smallest missing positive integer
            
        Raises:
            TypeError: If nums is not a list
        """
        if not isinstance(nums, list):
            raise TypeError("Input must be a list")
            
        array_length = len(nums)
        
        # Handle edge case of empty array
        if array_length == 0:
            return 1
            
        # Step 1: Replace non-positive numbers and numbers > n with a valid placeholder
        self._replace_invalid_numbers(nums, array_length)
        
        # Step 2: Use array indices to mark presence of numbers
        self._mark_number_presence(nums, array_length)
        
        # Step 3: Find first unmarked position
        return self._find_first_missing_positive(nums, array_length)
    
    def _replace_invalid_numbers(self, nums: list[int], array_length: int) -> None:
        """
        Replace numbers that are not in valid range [1, n] with a placeholder.
        
        Args:
            nums: The input array to modify in-place
            array_length: Length of the array
        """
        PLACEHOLDER_VALUE = array_length + 1
        
        for index in range(array_length):
            if nums[index] <= 0 or nums[index] > array_length:
                nums[index] = PLACEHOLDER_VALUE
    
    def _mark_number_presence(self, nums: list[int], array_length: int) -> None:
        """
        Mark presence of numbers by making corresponding indices negative.
        
        Args:
            nums: The array with valid positive numbers
            array_length: Length of the array
        """
        for current_index in range(array_length):
            target_number = abs(nums[current_index])
            
            # Only process numbers in valid range
            if target_number <= array_length:
                target_index = target_number - 1  # Convert to 0-based index
                
                # Mark presence by making the value at target_index negative
                if nums[target_index] > 0:
                    nums[target_index] = -nums[target_index]
    
    def _find_first_missing_positive(self, nums: list[int], array_length: int) -> int:
        """
        Find the first positive index that wasn't marked (still positive).
        
        Args:
            nums: The array after marking
            array_length: Length of the array
            
        Returns:
            The first missing positive integer
        """
        for index in range(array_length):
            if nums[index] > 0:  # This position wasn't marked
                return index + 1  # Convert back to 1-based numbering
        
        # All positions from 1 to n were marked, so n+1 is missing
        return array_length + 1