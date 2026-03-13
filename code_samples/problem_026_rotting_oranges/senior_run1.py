from typing import List, Tuple
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Calculate the minimum time for all fresh oranges to rot.
        
        Uses BFS to simulate the rotting process level by level, where each level
        represents one minute of time.
        
        Args:
            grid: 2D list where 0=empty, 1=fresh orange, 2=rotten orange
            
        Returns:
            Minimum minutes until all fresh oranges rot, or -1 if impossible
        """
        if not grid or not grid[0]:
            return 0
            
        rows_count = len(grid)
        columns_count = len(grid[0])
        fresh_oranges_count = 0
        rotten_queue = deque()
        
        # Initialize queue with all initially rotten oranges and count fresh ones
        for row_index in range(rows_count):
            for column_index in range(columns_count):
                if grid[row_index][column_index] == 2:
                    rotten_queue.append((row_index, column_index))
                elif grid[row_index][column_index] == 1:
                    fresh_oranges_count += 1
        
        # If no fresh oranges, no time needed
        if fresh_oranges_count == 0:
            return 0
            
        # If no rotten oranges but fresh ones exist, impossible to rot
        if not rotten_queue:
            return -1
            
        return self._simulate_rotting_process(
            grid, rotten_queue, fresh_oranges_count, rows_count, columns_count
        )
    
    def _simulate_rotting_process(
        self, 
        grid: List[List[int]], 
        rotten_queue: deque, 
        fresh_oranges_count: int,
        rows_count: int,
        columns_count: int
    ) -> int:
        """
        Simulate the BFS rotting process minute by minute.
        
        Args:
            grid: The orange grid to modify
            rotten_queue: Queue of initially rotten orange positions
            fresh_oranges_count: Count of fresh oranges to track
            rows_count: Number of rows in grid
            columns_count: Number of columns in grid
            
        Returns:
            Minutes elapsed or -1 if fresh oranges remain
        """
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        minutes_elapsed = 0
        
        while rotten_queue and fresh_oranges_count > 0:
            current_level_size = len(rotten_queue)  # Process all oranges at current minute
            
            for _ in range(current_level_size):
                current_row, current_column = rotten_queue.popleft()
                
                # Check all 4 adjacent cells
                for direction_row, direction_column in DIRECTIONS:
                    adjacent_row = current_row + direction_row
                    adjacent_column = current_column + direction_column
                    
                    if self._is_valid_fresh_orange(
                        grid, adjacent_row, adjacent_column, rows_count, columns_count
                    ):
                        grid[adjacent_row][adjacent_column] = 2  # Make it rotten
                        fresh_oranges_count -= 1
                        rotten_queue.append((adjacent_row, adjacent_column))
            
            minutes_elapsed += 1
        
        return minutes_elapsed if fresh_oranges_count == 0 else -1
    
    def _is_valid_fresh_orange(
        self, 
        grid: List[List[int]], 
        row: int, 
        column: int, 
        rows_count: int, 
        columns_count: int
    ) -> bool:
        """
        Check if the given position contains a fresh orange.
        
        Args:
            grid: The orange grid
            row: Row index to check
            column: Column index to check
            rows_count: Total number of rows
            columns_count: Total number of columns
            
        Returns:
            True if position is valid and contains a fresh orange
        """
        return (
            0 <= row < rows_count and 
            0 <= column < columns_count and 
            grid[row][column] == 1
        )