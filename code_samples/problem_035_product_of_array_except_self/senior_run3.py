from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Calculate the product of all elements except self for each element.
        
        Args:
            nums: List of integers
            
        Returns:
            List of integers where each element is the product of all other elements
            
        Raises:
            ValueError: If input array is empty or has less than 2 elements
        """
        if not nums or len(nums) < 2:
            raise ValueError("Input array must have at least 2 elements")
            
        array_length = len(nums)
        result_array = [1] * array_length
        
        # First pass: calculate left products
        self._calculate_left_products(nums, result_array, array_length)
        
        # Second pass: multiply by right products
        self._calculate_and_multiply_right_products(nums, result_array, array_length)
        
        return result_array
    
    def _calculate_left_products(self, nums: List[int], result_array: List[int], array_length: int) -> None:
        """
        Calculate cumulative products from left to right.
        
        Args:
            nums: Original input array
            result_array: Array to store intermediate results
            array_length: Length of the arrays
        """
        for current_index in range(1, array_length):
            # Each element gets the product of all elements to its left
            result_array[current_index] = result_array[current_index - 1] * nums[current_index - 1]
    
    def _calculate_and_multiply_right_products(self, nums: List[int], result_array: List[int], array_length: int) -> None:
        """
        Calculate cumulative products from right to left and multiply with existing left products.
        
        Args:
            nums: Original input array
            result_array: Array with left products to be updated
            array_length: Length of the arrays
        """
        right_product = 1
        
        for current_index in range(array_length - 1, -1, -1):
            # Multiply existing left product with right product
            result_array[current_index] *= right_product
            # Update right product for next iteration
            right_product *= nums[current_index]