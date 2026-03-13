from typing import List

class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Find the maximum coins that can be collected by bursting balloons optimally.
        
        Uses dynamic programming with interval DP approach. For each interval [left, right],
        we try bursting each balloon k in between and take the maximum.
        
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
        
        # Initialize memoization table
        memo_table = self._initialize_memo_table(balloon_count)
        
        # Solve using interval DP
        return self._solve_interval_dp(extended_nums, memo_table, 0, balloon_count - 1)
    
    def _add_boundary_balloons(self, nums: List[int]) -> List[int]:
        """
        Add boundary balloons with value 1 at both ends.
        
        Args:
            nums: Original balloon values
            
        Returns:
            Extended list with boundary balloons
        """
        return [1] + nums + [1]
    
    def _initialize_memo_table(self, size: int) -> List[List[int]]:
        """
        Initialize 2D memoization table with zeros.
        
        Args:
            size: Size of the table
            
        Returns:
            2D list initialized with zeros
        """
        return [[0] * size for _ in range(size)]
    
    def _solve_interval_dp(self, balloons: List[int], memo: List[List[int]], 
                          left_boundary: int, right_boundary: int) -> int:
        """
        Solve the interval DP problem recursively with memoization.
        
        For interval [left_boundary, right_boundary], try bursting each balloon
        in between as the last one to burst in this interval.
        
        Args:
            balloons: List of balloon values including boundaries
            memo: Memoization table
            left_boundary: Left boundary index (exclusive)
            right_boundary: Right boundary index (exclusive)
            
        Returns:
            Maximum coins for this interval
        """
        # Base case: no balloons to burst in this interval
        if left_boundary + 1 >= right_boundary:
            return 0
        
        # Return memoized result if already computed
        if memo[left_boundary][right_boundary] != 0:
            return memo[left_boundary][right_boundary]
        
        maximum_coins = 0
        
        # Try bursting each balloon as the last one in this interval
        for last_balloon_index in range(left_boundary + 1, right_boundary):
            coins_from_bursting = self._calculate_coins_from_burst(
                balloons, left_boundary, last_balloon_index, right_boundary
            )
            
            # Add coins from left and right subproblems
            left_subproblem_coins = self._solve_interval_dp(
                balloons, memo, left_boundary, last_balloon_index
            )
            right_subproblem_coins = self._solve_interval_dp(
                balloons, memo, last_balloon_index, right_boundary
            )
            
            total_coins = coins_from_bursting + left_subproblem_coins + right_subproblem_coins
            maximum_coins = max(maximum_coins, total_coins)
        
        # Memoize the result
        memo[left_boundary][right_boundary] = maximum_coins
        return maximum_coins
    
    def _calculate_coins_from_burst(self, balloons: List[int], left_idx: int, 
                                   burst_idx: int, right_idx: int) -> int:
        """
        Calculate coins obtained from bursting a specific balloon.
        
        When bursting balloon at burst_idx, it's adjacent to balloons
        at left_idx and right_idx (since all others in between are already burst).
        
        Args:
            balloons: List of balloon values
            left_idx: Index of left adjacent balloon
            burst_idx: Index of balloon being burst
            right_idx: Index of right adjacent balloon
            
        Returns:
            Coins obtained from this burst
        """
        return balloons[left_idx] * balloons[burst_idx] * balloons[right_idx]