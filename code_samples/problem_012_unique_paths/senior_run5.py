from typing import List

class Solution:
    """Solution for finding unique paths in a grid."""
    
    def uniquePaths(self, grid_rows: int, grid_cols: int) -> int:
        """
        Calculate the number of unique paths from top-left to bottom-right.
        
        Args:
            grid_rows: Number of rows in the grid
            grid_cols: Number of columns in the grid
            
        Returns:
            Number of unique paths from (0,0) to (grid_rows-1, grid_cols-1)
            
        Raises:
            ValueError: If grid dimensions are invalid
        """
        if grid_rows <= 0 or grid_cols <= 0:
            raise ValueError("Grid dimensions must be positive")
            
        if grid_rows == 1 or grid_cols == 1:
            return 1
            
        # Use dynamic programming with space optimization
        return self._calculate_paths_optimized(grid_rows, grid_cols)
    
    def _calculate_paths_optimized(self, total_rows: int, total_cols: int) -> int:
        """
        Calculate paths using space-optimized dynamic programming.
        
        Args:
            total_rows: Total number of rows
            total_cols: Total number of columns
            
        Returns:
            Number of unique paths
        """
        # Use 1D array to save space - only need previous row
        previous_row = [1] * total_cols  # First row is all 1s
        
        # Fill each subsequent row
        for current_row_index in range(1, total_rows):
            current_row = [1]  # First column is always 1
            
            for current_col_index in range(1, total_cols):
                # Paths = paths from above + paths from left
                paths_from_above = previous_row[current_col_index]
                paths_from_left = current_row[current_col_index - 1]
                current_row.append(paths_from_above + paths_from_left)
            
            previous_row = current_row
        
        return previous_row[total_cols - 1]
    
    def _calculate_paths_combinatorial(self, total_rows: int, total_cols: int) -> int:
        """
        Alternative solution using combinatorial mathematics.
        
        Args:
            total_rows: Total number of rows
            total_cols: Total number of columns
            
        Returns:
            Number of unique paths using C(m+n-2, m-1) formula
        """
        # Total moves needed: (total_rows - 1) down + (total_cols - 1) right
        total_moves = total_rows + total_cols - 2
        down_moves = total_rows - 1
        
        # Calculate combination C(total_moves, down_moves)
        return self._calculate_combination(total_moves, down_moves)
    
    def _calculate_combination(self, total_items: int, selected_items: int) -> int:
        """
        Calculate combination C(n, k) efficiently.
        
        Args:
            total_items: Total number of items (n)
            selected_items: Number of items to select (k)
            
        Returns:
            Combination value C(n, k)
        """
        if selected_items > total_items - selected_items:
            selected_items = total_items - selected_items  # Use smaller k for efficiency
        
        result = 1
        for iteration in range(selected_items):
            result = result * (total_items - iteration) // (iteration + 1)
        
        return result