from typing import List

class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Calculate the maximum coins that can be collected by bursting balloons.
        
        Uses dynamic programming with memoization to find the optimal order of
        bursting balloons to maximize coin collection.
        
        Args:
            nums: List of integers representing balloon values
            
        Returns:
            Maximum coins that can be collected
        """
        if not nums:
            return 0
            
        # Add boundary balloons with value 1
        extended_nums = self._prepare_balloon_array(nums)
        memo = {}
        
        return self._calculate_max_coins_recursive(
            extended_nums, 0, len(extended_nums) - 1, memo
        )
    
    def _prepare_balloon_array(self, nums: List[int]) -> List[int]:
        """
        Prepare the balloon array by adding boundary balloons with value 1.
        
        Args:
            nums: Original balloon values
            
        Returns:
            Extended array with boundary values
        """
        return [1] + nums + [1]
    
    def _calculate_max_coins_recursive(
        self, 
        balloons: List[int], 
        left_boundary: int, 
        right_boundary: int, 
        memo: dict
    ) -> int:
        """
        Recursively calculate maximum coins for a subrange of balloons.
        
        Args:
            balloons: Array of balloon values including boundaries
            left_boundary: Left boundary index (exclusive)
            right_boundary: Right boundary index (exclusive)
            memo: Memoization dictionary for caching results
            
        Returns:
            Maximum coins for the given subrange
        """
        # Base case: no balloons between boundaries
        if left_boundary + 1 >= right_boundary:
            return 0
        
        # Check memoization cache
        cache_key = (left_boundary, right_boundary)
        if cache_key in memo:
            return memo[cache_key]
        
        maximum_coins = 0
        
        # Try bursting each balloon as the last one in this range
        for last_balloon_index in range(left_boundary + 1, right_boundary):
            coins_from_left_subrange = self._calculate_max_coins_recursive(
                balloons, left_boundary, last_balloon_index, memo
            )
            coins_from_right_subrange = self._calculate_max_coins_recursive(
                balloons, last_balloon_index, right_boundary, memo
            )
            
            # Calculate coins from bursting this balloon last
            coins_from_current_balloon = (
                balloons[left_boundary] * 
                balloons[last_balloon_index] * 
                balloons[right_boundary]
            )
            
            total_coins = (
                coins_from_left_subrange + 
                coins_from_right_subrange + 
                coins_from_current_balloon
            )
            
            maximum_coins = max(maximum_coins, total_coins)
        
        # Cache and return result
        memo[cache_key] = maximum_coins
        return maximum_coins