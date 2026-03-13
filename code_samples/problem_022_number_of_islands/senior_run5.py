from typing import List

class Solution:
    """Solution for counting the number of islands in a 2D grid."""
    
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands in a 2D binary grid.
        
        An island is surrounded by water and is formed by connecting adjacent lands
        horizontally or vertically. You may assume all four edges of the grid are
        all surrounded by water.
        
        Args:
            grid: 2D list of strings where '1' represents land and '0' represents water
            
        Returns:
            The number of islands
            
        Raises:
            ValueError: If grid is empty or contains invalid values
        """
        if not grid or not grid[0]:
            return 0
            
        self._validate_grid(grid)
        
        rows = len(grid)
        columns = len(grid[0])
        visited_cells = set()
        island_count = 0
        
        for current_row in range(rows):
            for current_column in range(columns):
                if (current_row, current_column) not in visited_cells and grid[current_row][current_column] == '1':
                    self._explore_island(grid, current_row, current_column, visited_cells)
                    island_count += 1  # Found a new island
                    
        return island_count
    
    def _validate_grid(self, grid: List[List[str]]) -> None:
        """
        Validate that the grid contains only valid values.
        
        Args:
            grid: 2D list of strings to validate
            
        Raises:
            ValueError: If grid contains invalid values
        """
        for row in grid:
            for cell in row:
                if cell not in ('0', '1'):
                    raise ValueError(f"Invalid grid value: {cell}. Only '0' and '1' are allowed.")
    
    def _explore_island(self, grid: List[List[str]], start_row: int, start_column: int, visited_cells: set) -> None:
        """
        Perform DFS to mark all cells belonging to the same island as visited.
        
        Args:
            grid: 2D list representing the map
            start_row: Starting row position
            start_column: Starting column position
            visited_cells: Set to track visited positions
        """
        rows = len(grid)
        columns = len(grid[0])
        exploration_stack = [(start_row, start_column)]
        
        # Directions for adjacent cells: up, down, left, right
        ADJACENT_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while exploration_stack:
            current_row, current_column = exploration_stack.pop()
            
            # Skip if already visited or out of bounds
            if (current_row, current_column) in visited_cells:
                continue
                
            if (current_row < 0 or current_row >= rows or 
                current_column < 0 or current_column >= columns or
                grid[current_row][current_column] == '0'):
                continue
                
            visited_cells.add((current_row, current_column))  # Mark as visited
            
            # Add all adjacent land cells to exploration stack
            for row_delta, column_delta in ADJACENT_DIRECTIONS:
                next_row = current_row + row_delta
                next_column = current_column + column_delta
                exploration_stack.append((next_row, next_column))