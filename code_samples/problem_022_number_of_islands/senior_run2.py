from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands in a 2D binary grid.
        
        An island is formed by connecting adjacent lands horizontally or vertically.
        Uses DFS to explore and mark visited land cells.
        
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
        
        total_rows = len(grid)
        total_columns = len(grid[0])
        island_count = 0
        
        for current_row in range(total_rows):
            for current_column in range(total_columns):
                if grid[current_row][current_column] == '1':
                    self._explore_island_dfs(grid, current_row, current_column, total_rows, total_columns)
                    island_count += 1  # Found a new island
                    
        return island_count
    
    def _explore_island_dfs(self, grid: List[List[str]], row: int, column: int, 
                           total_rows: int, total_columns: int) -> None:
        """
        Explore and mark all connected land cells using depth-first search.
        
        Args:
            grid: 2D binary grid to modify
            row: Current row position
            column: Current column position
            total_rows: Total number of rows in grid
            total_columns: Total number of columns in grid
        """
        # Check bounds and if current cell is water or already visited
        if (row < 0 or row >= total_rows or 
            column < 0 or column >= total_columns or 
            grid[row][column] != '1'):
            return
            
        # Mark current land cell as visited
        grid[row][column] = '0'
        
        # Define directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Explore all adjacent cells
        for delta_row, delta_column in directions:
            next_row = row + delta_row
            next_column = column + delta_column
            self._explore_island_dfs(grid, next_row, next_column, total_rows, total_columns)
    
    def _validate_grid(self, grid: List[List[str]]) -> None:
        """
        Validate that grid contains only '0' and '1' characters.
        
        Args:
            grid: 2D grid to validate
            
        Raises:
            ValueError: If grid contains invalid characters
        """
        valid_values = {'0', '1'}
        
        for row_index, row in enumerate(grid):
            for column_index, cell_value in enumerate(row):
                if cell_value not in valid_values:
                    raise ValueError(
                        f"Invalid cell value '{cell_value}' at position ({row_index}, {column_index}). "
                        f"Expected '0' or '1'."
                    )