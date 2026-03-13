from typing import List

class Solution:
    def uniquePaths(self, grid_rows: int, grid_cols: int) -> int:
        """
        Calculate the number of unique paths from top-left to bottom-right corner.
        
        The robot can only move right or down in an m x n grid.
        
        Args:
            grid_rows: Number of rows in the grid
            grid_cols: Number of columns in the grid
            
        Returns:
            Number of unique paths from (0,0) to (m-1,n-1)
            
        Raises:
            ValueError: If grid dimensions are invalid
        """
        if grid_rows <= 0 or grid_cols <= 0:
            raise ValueError("Grid dimensions must be positive integers")
            
        if grid_rows == 1 or grid_cols == 1:
            return 1
            
        return self._calculate_paths_dynamic_programming(grid_rows, grid_cols)
    
    def _calculate_paths_dynamic_programming(self, total_rows: int, total_cols: int) -> int:
        """
        Use dynamic programming to calculate unique paths efficiently.
        
        Args:
            total_rows: Total number of rows in grid
            total_cols: Total number of columns in grid
            
        Returns:
            Number of unique paths using DP approach
        """
        # Initialize DP table with base cases
        dp_table = [[0] * total_cols for _ in range(total_rows)]
        
        # Fill first row - only one way to reach any cell in first row
        for column_index in range(total_cols):
            dp_table[0][column_index] = 1
            
        # Fill first column - only one way to reach any cell in first column  
        for row_index in range(total_rows):
            dp_table[row_index][0] = 1
            
        # Fill remaining cells using recurrence relation
        for current_row in range(1, total_rows):
            for current_col in range(1, total_cols):
                # Paths = paths from above + paths from left
                paths_from_above = dp_table[current_row - 1][current_col]
                paths_from_left = dp_table[current_row][current_col - 1]
                dp_table[current_row][current_col] = paths_from_above + paths_from_left
                
        return dp_table[total_rows - 1][total_cols - 1]