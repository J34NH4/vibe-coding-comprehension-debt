from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Calculate the product of all elements except self for each position.
        
        Uses a two-pass approach to avoid division:
        1. Left pass: Calculate products of all elements to the left
        2. Right pass: Calculate products of all elements to the right
        
        Args:
            nums: List of integers
            
        Returns:
            List where each element is the product of all other elements
            
        Time Complexity: O(n)
        Space Complexity: O(1) excluding output array
        """
        if not nums:
            return []
            
        array_length = len(nums)
        result_array = [1] * array_length
        
        # Left pass: Calculate products of elements to the left of each index
        left_product = 1
        for current_index in range(array_length):
            result_array[current_index] = left_product
            left_product *= nums[current_index]  # Update for next iteration
            
        # Right pass: Multiply by products of elements to the right
        right_product = 1
        for current_index in range(array_length - 1, -1, -1):
            result_array[current_index] *= right_product  # Combine left and right products
            right_product *= nums[current_index]  # Update for next iteration
            
        return result_array