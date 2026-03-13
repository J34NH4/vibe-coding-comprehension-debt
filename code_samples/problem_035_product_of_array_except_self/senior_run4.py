from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Calculate the product of all elements except self for each position.
        
        Uses two-pass approach with left and right products to avoid division.
        Time complexity: O(n), Space complexity: O(1) excluding output array.
        
        Args:
            nums: List of integers
            
        Returns:
            List of integers where each element is the product of all other elements
        """
        if not nums:
            return []
            
        array_length = len(nums)
        result_array = [1] * array_length
        
        # First pass: calculate left products
        left_product = 1
        for current_index in range(array_length):
            result_array[current_index] = left_product  # Product of all elements to the left
            left_product *= nums[current_index]
        
        # Second pass: multiply by right products
        right_product = 1
        for current_index in range(array_length - 1, -1, -1):
            result_array[current_index] *= right_product  # Multiply by product of all elements to the right
            right_product *= nums[current_index]
            
        return result_array