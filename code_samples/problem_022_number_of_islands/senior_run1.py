from typing import List


class Solution:
    """Solution for counting the number of islands in a 2D grid."""
    
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands in a 2D binary grid.
        
        Args:
            grid: 2D list of strings where '1' represents land and '0' represents water
            
        Returns:
            Number of islands (connected components of '1's)
            
        Raises:
            ValueError: If grid is empty or invalid
        """
        if not grid or not grid[0]:
            return 0
            
        total_rows = len(grid)
        total_columns = len(grid[0])
        island_count = 0
        
        for current_row in range(total_rows):
            for current_column in range(total_columns):
                if grid[current_row][current_column] == '1':
                    # Found start of new island - mark entire island as visited
                    self._mark_island_as_visited(grid, current_row, current_column, total_rows, total_columns)
                    island_count += 1
                    
        return island_count
    
    def _mark_island_as_visited(self, grid: List[List[str]], row: int, column: int, 
                               total_rows: int, total_columns: int) -> None:
        """
        Mark all connected land cells as visited using DFS.
        
        Args:
            grid: 2D grid to modify
            row: Current row position
            column: Current column position
            total_rows: Total number of rows in grid
            total_columns: Total number of columns in grid
        """
        # Check bounds and if current cell is water or already visited
        if (row < 0 or row >= total_rows or 
            column < 0 or column >= total_columns or 
            grid[row][column] == '0'):
            return
            
        # Mark current cell as visited by setting to '0'
        grid[row][column] = '0'
        
        # Recursively visit all 4 adjacent cells
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        for row_delta, column_delta in directions:
            next_row = row + row_delta
            next_column = column + column_delta
            self._mark_island_as_visited(grid, next_row, next_column, total_rows, total_columns)