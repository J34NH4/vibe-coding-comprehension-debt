from typing import List

class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Calculate the maximum coins obtainable by bursting balloons optimally.
        
        Uses dynamic programming with memoization. The key insight is to think
        about which balloon to burst LAST in each subarray, rather than first.
        
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
    
    def _calculate_max_coins(self, extended_nums: List[int], left: int, right: int, memo: dict) -> int:
        """
        Calculate maximum coins for bursting balloons between left and right indices.
        
        Args:
            extended_nums: Balloon array with boundary values
            left: Left boundary index (exclusive)
            right: Right boundary index (exclusive)
            memo: Memoization dictionary
            
        Returns:
            Maximum coins obtainable in the range
        """
        # Base case: no balloons between left and right
        if left + 1 >= right:
            return 0
            
        # Check memoization cache
        cache_key = (left, right)
        if cache_key in memo:
            return memo[cache_key]
        
        maximum_coins = 0
        
        # Try bursting each balloon as the LAST one in this range
        for last_balloon_index in range(left + 1, right):
            # Coins from bursting this balloon last
            coins_from_burst = (extended_nums[left] * 
                              extended_nums[last_balloon_index] * 
                              extended_nums[right])
            
            # Recursively calculate coins from left and right subarrays
            left_subarray_coins = self._calculate_max_coins(extended_nums, left, last_balloon_index, memo)
            right_subarray_coins = self._calculate_max_coins(extended_nums, last_balloon_index, right, memo)
            
            total_coins = coins_from_burst + left_subarray_coins + right_subarray_coins
            maximum_coins = max(maximum_coins, total_coins)
        
        # Store result in memoization cache
        memo[cache_key] = maximum_coins
        return maximum_coins