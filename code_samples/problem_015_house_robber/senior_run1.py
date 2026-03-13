from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Calculate the maximum amount that can be robbed without robbing adjacent houses.
        
        Uses dynamic programming approach where for each house, we decide whether to rob it
        or skip it based on maximum profit achievable.
        
        Args:
            nums: List of integers representing money in each house
            
        Returns:
            Maximum amount that can be robbed
            
        Raises:
            ValueError: If nums is None
        """
        if nums is None:
            raise ValueError("Input array cannot be None")
            
        if not nums:
            return 0
            
        if len(nums) == 1:
            return nums[0]
            
        return self._calculate_max_robbery_amount(nums)
    
    def _calculate_max_robbery_amount(self, house_values: List[int]) -> int:
        """
        Calculate maximum robbery amount using dynamic programming.
        
        For each house, we have two choices:
        1. Rob current house + max from houses before previous house
        2. Skip current house and take max from previous house
        
        Args:
            house_values: List of money amounts in each house
            
        Returns:
            Maximum amount that can be robbed
        """
        previous_max = 0  # Maximum amount up to house i-2
        current_max = 0   # Maximum amount up to house i-1
        
        for house_value in house_values:
            # Either rob current house + previous_max, or skip current house
            new_max = max(house_value + previous_max, current_max)
            previous_max = current_max  # Update for next iteration
            current_max = new_max       # Update current maximum
            
        return current_max