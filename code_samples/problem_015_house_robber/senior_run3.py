from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Calculate maximum amount that can be robbed without robbing adjacent houses.
        
        Uses dynamic programming to track maximum profit at each position.
        At each house, we choose between robbing current house + profit from
        house before previous, or keeping profit from previous house.
        
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
    
    def _calculate_max_robbery_amount(self, house_values: List[int]) -> int:
        """
        Calculate maximum robbery amount using space-optimized dynamic programming.
        
        Args:
            house_values: List of money amounts in each house
            
        Returns:
            Maximum amount that can be robbed
        """
        if len(house_values) == 1:
            return house_values[0]
        
        # Track maximum profit from previous two positions
        previous_max = 0  # Maximum profit excluding previous house
        current_max = 0   # Maximum profit including/excluding current house
        
        for house_value in house_values:
            # Calculate new maximum: either rob current house + previous_max
            # or keep current_max (don't rob current house)
            new_max = max(current_max, previous_max + house_value)
            previous_max = current_max  # Update for next iteration
            current_max = new_max
            
        return current_max