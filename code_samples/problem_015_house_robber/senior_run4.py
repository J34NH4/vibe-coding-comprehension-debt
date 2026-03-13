from typing import List


class Solution:
    """Solution for the House Robber problem using dynamic programming."""
    
    def rob(self, nums: List[int]) -> int:
        """
        Calculate the maximum amount that can be robbed without robbing adjacent houses.
        
        Uses dynamic programming approach where for each house, we decide whether
        to rob it or not based on maximum profit from previous calculations.
        
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
        
        return self._calculate_max_robbery(nums)
    
    def _calculate_max_robbery(self, house_values: List[int]) -> int:
        """
        Helper method to calculate maximum robbery amount using dynamic programming.
        
        For each house, we maintain two values:
        - previous_max: Maximum amount robbed up to previous house
        - current_max: Maximum amount robbed up to current house
        
        Args:
            house_values: List of house values
            
        Returns:
            Maximum amount that can be robbed
        """
        previous_max = 0  # Maximum amount robbed up to house i-2
        current_max = 0   # Maximum amount robbed up to house i-1
        
        for house_value in house_values:
            # For current house, decide: rob it + previous_max OR skip it and keep current_max
            new_max = max(current_max, previous_max + house_value)
            previous_max = current_max  # Update previous maximum
            current_max = new_max       # Update current maximum
            
        return current_max