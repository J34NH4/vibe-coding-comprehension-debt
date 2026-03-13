from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Calculate the maximum coins that can be collected by bursting balloons.
        
        Uses dynamic programming with memoization. For each subproblem defined by
        left and right boundaries, tries bursting each balloon as the last one
        and takes the maximum result.
        
        Args:
            nums: List of integers representing balloon values
            
        Returns:
            Maximum coins that can be collected
            
        Raises:
            ValueError: If nums is None
        """
        if nums is None:
            raise ValueError("Input cannot be None")
            
        if not nums:
            return 0
            
        # Add boundary balloons with value 1
        extended_nums = [1] + nums + [1]
        memo = {}
        
        return self._calculate_max_coins(extended_nums, 0, len(extended_nums) - 1, memo)
    
    def _calculate_max_coins(self, extended_nums: List[int], left_boundary: int, 
                           right_boundary: int, memo: dict) -> int:
        """
        Calculate maximum coins for balloons between left_boundary and right_boundary.
        
        Uses memoization to avoid recalculating the same subproblems. For each
        possible last balloon to burst, calculates the total coins and returns
        the maximum.
        
        Args:
            extended_nums: Original nums with boundary balloons added
            left_boundary: Left boundary index (exclusive)
            right_boundary: Right boundary index (exclusive)
            memo: Dictionary for memoization
            
        Returns:
            Maximum coins for the given range
        """
        # Base case: no balloons between boundaries
        if left_boundary + 1 >= right_boundary:
            return 0
            
        # Check memoization cache
        cache_key = (left_boundary, right_boundary)
        if cache_key in memo:
            return memo[cache_key]
        
        max_coins = 0
        
        # Try bursting each balloon as the last one in this range
        for last_balloon_index in range(left_boundary + 1, right_boundary):
            # Coins from bursting this balloon last
            coins_from_burst = (extended_nums[left_boundary] * 
                              extended_nums[last_balloon_index] * 
                              extended_nums[right_boundary])
            
            # Coins from left subproblem
            left_coins = self._calculate_max_coins(extended_nums, left_boundary, 
                                                 last_balloon_index, memo)
            
            # Coins from right subproblem  
            right_coins = self._calculate_max_coins(extended_nums, last_balloon_index, 
                                                  right_boundary, memo)
            
            total_coins = coins_from_burst + left_coins + right_coins
            max_coins = max(max_coins, total_coins)
        
        # Store in memo and return
        memo[cache_key] = max_coins
        return max_coins