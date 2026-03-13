from typing import List

class Solution:
    """Solution for finding unique paths in a grid with movement constraints."""
    
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Calculate the number of unique paths from top-left to bottom-right corner.
        
        Robot can only move right or down in an m x n grid.
        
        Args:
            m: Number of rows in the grid
            n: Number of columns in the grid
            
        Returns:
            Number of unique paths from (0,0) to (m-1, n-1)
            
        Raises:
            ValueError: If m or n is less than 1
        """
        if m < 1 or n < 1:
            raise ValueError("Grid dimensions must be at least 1x1")
            
        return self._calculate_paths_dynamic_programming(m, n)
    
    def _calculate_paths_dynamic_programming(self, rows: int, columns: int) -> int:
        """
        Use dynamic programming to calculate unique paths efficiently.
        
        Args:
            rows: Number of rows in the grid
            columns: Number of columns in the grid
            
        Returns:
            Number of unique paths
        """
        # Initialize DP table with base cases
        dp_table = self._initialize_dp_table(rows, columns)
        
        # Fill the DP table using recurrence relation
        for current_row in range(1, rows):
            for current_column in range(1, columns):
                # Paths to current cell = paths from above + paths from left
                dp_table[current_row][current_column] = (
                    dp_table[current_row - 1][current_column] + 
                    dp_table[current_row][current_column - 1]
                )
        
        return dp_table[rows - 1][columns - 1]
    
    def _initialize_dp_table(self, rows: int, columns: int) -> List[List[int]]:
        """
        Initialize the dynamic programming table with base cases.
        
        Args:
            rows: Number of rows needed
            columns: Number of columns needed
            
        Returns:
            2D list initialized with base cases (1s in first row and column)
        """
        dp_table = [[0] * columns for _ in range(rows)]
        
        # Base case: First row - only one way to reach any cell (move right)
        for column_index in range(columns):
            dp_table[0][column_index] = 1
            
        # Base case: First column - only one way to reach any cell (move down)
        for row_index in range(rows):
            dp_table[row_index][0] = 1
            
        return dp_table