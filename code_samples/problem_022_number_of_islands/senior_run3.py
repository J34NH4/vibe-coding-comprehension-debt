from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands in a 2D binary grid.
        
        An island is a group of connected '1's surrounded by '0's or boundaries.
        Uses DFS to explore and mark visited land cells.
        
        Args:
            grid: 2D binary grid where '1' represents land and '0' represents water
            
        Returns:
            Number of islands found in the grid
            
        Raises:
            ValueError: If grid is empty or contains invalid characters
        """
        if not grid or not grid[0]:
            return 0
            
        self._validate_grid(grid)
        
        number_of_rows = len(grid)
        number_of_columns = len(grid[0])
        island_count = 0
        
        for current_row in range(number_of_rows):
            for current_column in range(number_of_columns):
                if grid[current_row][current_column] == '1':
                    # Found unvisited land - start new island exploration
                    self._explore_island_dfs(grid, current_row, current_column, number_of_rows, number_of_columns)
                    island_count += 1
                    
        return island_count
    
    def _explore_island_dfs(self, grid: List[List[str]], row: int, column: int, 
                           total_rows: int, total_columns: int) -> None:
        """
        Explore an island using depth-first search and mark visited cells.
        
        Args:
            grid: 2D binary grid to explore
            row: Current row position
            column: Current column position
            total_rows: Total number of rows in grid
            total_columns: Total number of columns in grid
        """
        # Check boundary conditions and water cells
        if (row < 0 or row >= total_rows or 
            column < 0 or column >= total_columns or 
            grid[row][column] == '0'):
            return
            
        # Mark current land cell as visited by changing to water
        grid[row][column] = '0'
        
        # Explore all four adjacent directions
        direction_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for row_offset, column_offset in direction_offsets:
            next_row = row + row_offset
            next_column = column + column_offset
            self._explore_island_dfs(grid, next_row, next_column, total_rows, total_columns)
    
    def _validate_grid(self, grid: List[List[str]]) -> None:
        """
        Validate that grid contains only valid characters.
        
        Args:
            grid: 2D grid to validate
            
        Raises:
            ValueError: If grid contains invalid characters
        """
        valid_characters = {'0', '1'}
        for row in grid:
            for cell_value in row:
                if cell_value not in valid_characters:
                    raise ValueError(f"Invalid character '{cell_value}' found in grid. Only '0' and '1' are allowed.")