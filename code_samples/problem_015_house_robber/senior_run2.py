from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Calculate the maximum amount that can be robbed without robbing adjacent houses.
        
        Uses dynamic programming to track the maximum profit at each position,
        considering whether to rob the current house or skip it.
        
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
        Calculate maximum robbery amount using optimized space complexity.
        
        Args:
            house_values: List of money amounts in each house
            
        Returns:
            Maximum amount that can be robbed
        """
        # Track maximum profit including and excluding previous house
        max_profit_including_previous = house_values[0]
        max_profit_excluding_previous = 0
        
        for current_house_index in range(1, len(house_values)):
            current_house_value = house_values[current_house_index]
            
            # Current max if we rob this house = previous excluding + current value
            current_max_including = max_profit_excluding_previous + current_house_value
            
            # Update for next iteration
            max_profit_excluding_previous = max_profit_including_previous
            max_profit_including_previous = max(current_max_including, max_profit_including_previous)
        
        return max_profit_including_previous