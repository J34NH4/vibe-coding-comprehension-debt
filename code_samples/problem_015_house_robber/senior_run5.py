from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Calculate maximum amount that can be robbed without robbing adjacent houses.
        
        Args:
            nums: List of integers representing money in each house
            
        Returns:
            Maximum amount that can be robbed
            
        Raises:
            ValueError: If nums is empty
        """
        if not nums:
            raise ValueError("Input array cannot be empty")
        
        return self._calculate_max_robbery_amount(nums)
    
    def _calculate_max_robbery_amount(self, house_amounts: List[int]) -> int:
        """
        Use dynamic programming to find optimal robbery strategy.
        
        Args:
            house_amounts: List of money amounts in each house
            
        Returns:
            Maximum robbery amount possible
        """
        house_count = len(house_amounts)
        
        # Base cases
        if house_count == 1:
            return house_amounts[0]
        if house_count == 2:
            return max(house_amounts[0], house_amounts[1])
        
        # Initialize DP variables
        previous_max = house_amounts[0]  # Max amount up to house i-2
        current_max = max(house_amounts[0], house_amounts[1])  # Max amount up to house i-1
        
        # Calculate optimal amount for each house
        for current_house_index in range(2, house_count):
            current_house_amount = house_amounts[current_house_index]
            
            # Either rob current house + max from i-2, or skip current house
            new_max = max(current_max, previous_max + current_house_amount)
            
            # Update for next iteration
            previous_max = current_max
            current_max = new_max
        
        return current_max