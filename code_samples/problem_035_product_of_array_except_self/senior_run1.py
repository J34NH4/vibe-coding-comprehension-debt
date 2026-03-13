from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Calculate the product of all elements except self for each position.
        
        Uses two-pass approach: left products, then right products.
        Time complexity: O(n), Space complexity: O(1) excluding output array.
        
        Args:
            nums: List of integers
            
        Returns:
            List where each element is product of all other elements
        """
        if not nums:
            return []
            
        array_length = len(nums)
        result_array = [1] * array_length
        
        # First pass: calculate left products
        left_product = 1
        for current_index in range(array_length):
            result_array[current_index] = left_product
            left_product *= nums[current_index]  # Update for next iteration
            
        # Second pass: multiply by right products
        right_product = 1
        for current_index in range(array_length - 1, -1, -1):
            result_array[current_index] *= right_product
            right_product *= nums[current_index]  # Update for next iteration
            
        return result_array