from typing import List

class Solution:
    """Solution for counting the number of islands in a 2D grid."""
    
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands in a 2D binary grid.
        
        An island is surrounded by water and is formed by connecting adjacent lands
        horizontally or vertically. All four edges of the grid are surrounded by water.
        
        Args:
            grid: 2D binary grid where '1' represents land and '0' represents water
            
        Returns:
            Number of islands found in the grid
            
        Raises:
            ValueError: If grid is empty or contains invalid values
        """
        if not grid or not grid[0]:
            return 0
            
        self._validate_grid(grid)
        
        island_count = 0
        rows = len(grid)
        columns = len(grid[0])
        
        for current_row in range(rows):
            for current_column in range(columns):
                if grid[current_row][current_column] == '1':
                    self._mark_island_as_visited(grid, current_row, current_column, rows, columns)
                    island_count += 1  # Found a new island
                    
        return island_count
    
    def _validate_grid(self, grid: List[List[str]]) -> None:
        """
        Validate that the grid contains only '0' and '1' values.
        
        Args:
            grid: 2D grid to validate
            
        Raises:
            ValueError: If grid contains invalid values
        """
        for row in grid:
            for cell in row:
                if cell not in ['0', '1']:
                    raise ValueError(f"Invalid grid value: {cell}. Only '0' and '1' are allowed.")
    
    def _mark_island_as_visited(self, grid: List[List[str]], row: int, column: int, 
                               total_rows: int, total_columns: int) -> None:
        """
        Use DFS to mark all connected land cells as visited by setting them to '0'.
        
        Args:
            grid: 2D grid being processed
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
            
        # Mark current land cell as visited
        grid[row][column] = '0'
        
        # Explore all four adjacent cells (up, down, left, right)
        adjacent_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for row_delta, column_delta in adjacent_directions:
            next_row = row + row_delta
            next_column = column + column_delta
            self._mark_island_as_visited(grid, next_row, next_column, total_rows, total_columns)