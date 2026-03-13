from typing import List

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Calculate the number of unique paths from top-left to bottom-right in an m x n grid.
        
        The robot can only move right or down at any point in time.
        
        Args:
            m: Number of rows in the grid
            n: Number of columns in the grid
            
        Returns:
            Number of unique paths from (0,0) to (m-1,n-1)
            
        Raises:
            ValueError: If m or n is less than 1
        """
        if m < 1 or n < 1:
            raise ValueError("Grid dimensions must be at least 1x1")
            
        return self._calculate_paths_dynamic_programming(m, n)
    
    def _calculate_paths_dynamic_programming(self, rows: int, columns: int) -> int:
        """
        Use dynamic programming to calculate unique paths.
        
        Args:
            rows: Number of rows in the grid
            columns: Number of columns in the grid
            
        Returns:
            Number of unique paths
        """
        # Create DP table where dp[i][j] represents paths to reach cell (i,j)
        dp_table = [[0] * columns for _ in range(rows)]
        
        # Initialize first row - only one way to reach any cell in first row
        for column_index in range(columns):
            dp_table[0][column_index] = 1
            
        # Initialize first column - only one way to reach any cell in first column
        for row_index in range(rows):
            dp_table[row_index][0] = 1
            
        # Fill the DP table
        for current_row in range(1, rows):
            for current_column in range(1, columns):
                # Paths to current cell = paths from above + paths from left
                paths_from_above = dp_table[current_row - 1][current_column]
                paths_from_left = dp_table[current_row][current_column - 1]
                dp_table[current_row][current_column] = paths_from_above + paths_from_left
                
        return dp_table[rows - 1][columns - 1]