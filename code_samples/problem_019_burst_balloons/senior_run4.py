from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Calculate the maximum coins that can be collected by bursting balloons optimally.
        
        Uses dynamic programming with interval DP approach. For each interval [left, right],
        we try bursting each balloon k as the last one in that interval.
        
        Args:
            nums: List of integers representing balloon values
            
        Returns:
            Maximum coins that can be collected
        """
        if not nums:
            return 0
            
        # Add boundary balloons with value 1
        extended_nums = self._add_boundary_balloons(nums)
        balloon_count = len(extended_nums)
        
        # dp[left][right] = max coins from bursting balloons in open interval (left, right)
        dp_table = [[0] * balloon_count for _ in range(balloon_count)]
        
        return self._calculate_max_coins(extended_nums, dp_table, balloon_count)
    
    def _add_boundary_balloons(self, nums: List[int]) -> List[int]:
        """
        Add boundary balloons with value 1 at both ends.
        
        Args:
            nums: Original balloon values
            
        Returns:
            Extended list with boundary balloons
        """
        return [1] + nums + [1]
    
    def _calculate_max_coins(self, extended_nums: List[int], dp_table: List[List[int]], 
                           balloon_count: int) -> int:
        """
        Fill the DP table using interval dynamic programming.
        
        Args:
            extended_nums: Balloon values with boundaries
            dp_table: 2D DP table to fill
            balloon_count: Total number of balloons including boundaries
            
        Returns:
            Maximum coins from optimal balloon bursting
        """
        # Iterate over all possible interval lengths
        for interval_length in range(2, balloon_count):
            for left_boundary in range(balloon_count - interval_length):
                right_boundary = left_boundary + interval_length
                
                # Try bursting each balloon k as the last one in interval (left_boundary, right_boundary)
                for last_balloon in range(left_boundary + 1, right_boundary):
                    current_coins = self._calculate_coins_for_burst(
                        extended_nums, dp_table, left_boundary, right_boundary, last_balloon
                    )
                    
                    dp_table[left_boundary][right_boundary] = max(
                        dp_table[left_boundary][right_boundary], 
                        current_coins
                    )
        
        return dp_table[0][balloon_count - 1]
    
    def _calculate_coins_for_burst(self, extended_nums: List[int], dp_table: List[List[int]],
                                 left_boundary: int, right_boundary: int, 
                                 last_balloon: int) -> int:
        """
        Calculate coins gained by bursting a specific balloon last in an interval.
        
        Args:
            extended_nums: Balloon values with boundaries
            dp_table: Current state of DP table
            left_boundary: Left boundary of interval
            right_boundary: Right boundary of interval
            last_balloon: Index of balloon to burst last
            
        Returns:
            Total coins from this bursting strategy
        """
        # Coins from bursting the last balloon (adjacent balloons will be boundaries)
        burst_coins = (extended_nums[left_boundary] * 
                      extended_nums[last_balloon] * 
                      extended_nums[right_boundary])
        
        # Add coins from optimal bursting of left and right sub-intervals
        left_interval_coins = dp_table[left_boundary][last_balloon]
        right_interval_coins = dp_table[last_balloon][right_boundary]
        
        return burst_coins + left_interval_coins + right_interval_coins