from typing import List
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Determines the minimum time for all oranges to rot using BFS.
        
        Args:
            grid: 2D grid where 0=empty, 1=fresh orange, 2=rotten orange
            
        Returns:
            Minimum minutes for all oranges to rot, or -1 if impossible
        """
        if not grid or not grid[0]:
            return 0
            
        rows_count = len(grid)
        cols_count = len(grid[0])
        fresh_oranges_count = 0
        rotten_queue = deque()
        
        # Initialize queue with rotten oranges and count fresh ones
        for row_index in range(rows_count):
            for col_index in range(cols_count):
                if grid[row_index][col_index] == 1:
                    fresh_oranges_count += 1
                elif grid[row_index][col_index] == 2:
                    rotten_queue.append((row_index, col_index))
        
        # No fresh oranges to rot
        if fresh_oranges_count == 0:
            return 0
            
        # No rotten oranges to spread
        if not rotten_queue:
            return -1
            
        return self._simulate_rotting_process(grid, rotten_queue, fresh_oranges_count, rows_count, cols_count)
    
    def _simulate_rotting_process(self, grid: List[List[int]], rotten_queue: deque, 
                                fresh_oranges_count: int, rows_count: int, cols_count: int) -> int:
        """
        Simulates the rotting process using BFS.
        
        Args:
            grid: The orange grid
            rotten_queue: Queue of initially rotten orange positions
            fresh_oranges_count: Count of fresh oranges
            rows_count: Number of rows in grid
            cols_count: Number of columns in grid
            
        Returns:
            Minutes elapsed for all oranges to rot, or -1 if impossible
        """
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        minutes_elapsed = 0
        
        while rotten_queue and fresh_oranges_count > 0:
            current_level_size = len(rotten_queue)  # Process all oranges that rot at current minute
            
            for _ in range(current_level_size):
                current_row, current_col = rotten_queue.popleft()
                
                # Check all adjacent cells
                for direction_row, direction_col in DIRECTIONS:
                    adjacent_row = current_row + direction_row
                    adjacent_col = current_col + direction_col
                    
                    if self._is_valid_fresh_orange(grid, adjacent_row, adjacent_col, rows_count, cols_count):
                        grid[adjacent_row][adjacent_col] = 2  # Make it rotten
                        fresh_oranges_count -= 1
                        rotten_queue.append((adjacent_row, adjacent_col))
            
            minutes_elapsed += 1
        
        return minutes_elapsed if fresh_oranges_count == 0 else -1
    
    def _is_valid_fresh_orange(self, grid: List[List[int]], row: int, col: int, 
                             rows_count: int, cols_count: int) -> bool:
        """
        Checks if the given position contains a fresh orange.
        
        Args:
            grid: The orange grid
            row: Row index to check
            col: Column index to check
            rows_count: Total number of rows
            cols_count: Total number of columns
            
        Returns:
            True if position is valid and contains a fresh orange
        """
        return (0 <= row < rows_count and 
                0 <= col < cols_count and 
                grid[row][col] == 1)