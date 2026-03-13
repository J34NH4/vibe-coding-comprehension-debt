from typing import List, Tuple
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Determines the minimum time for all oranges to rot using BFS.
        
        Args:
            grid: 2D list where 0=empty, 1=fresh orange, 2=rotten orange
            
        Returns:
            Minimum minutes for all oranges to rot, or -1 if impossible
        """
        if not grid or not grid[0]:
            return 0
            
        rows, cols = len(grid), len(grid[0])
        fresh_count = 0
        rotten_queue = deque()
        
        # Find all rotten oranges and count fresh ones
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    fresh_count += 1
                elif grid[row][col] == 2:
                    rotten_queue.append((row, col))
        
        # No fresh oranges to rot
        if fresh_count == 0:
            return 0
            
        # No rotten oranges but fresh ones exist
        if not rotten_queue:
            return -1
            
        return self._simulate_rotting_process(grid, rotten_queue, fresh_count)
    
    def _simulate_rotting_process(self, grid: List[List[int]], rotten_queue: deque, fresh_count: int) -> int:
        """
        Simulates the rotting process using BFS.
        
        Args:
            grid: The orange grid
            rotten_queue: Queue of initially rotten orange positions
            fresh_count: Number of fresh oranges
            
        Returns:
            Minutes elapsed or -1 if impossible
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        minutes_elapsed = 0
        rows, cols = len(grid), len(grid[0])
        
        while rotten_queue and fresh_count > 0:
            minutes_elapsed += 1
            current_level_size = len(rotten_queue)
            
            # Process all oranges that rot in this minute
            for _ in range(current_level_size):
                current_row, current_col = rotten_queue.popleft()
                
                # Check all adjacent cells
                for delta_row, delta_col in directions:
                    adjacent_row = current_row + delta_row
                    adjacent_col = current_col + delta_col
                    
                    if self._is_valid_fresh_orange(grid, adjacent_row, adjacent_col, rows, cols):
                        grid[adjacent_row][adjacent_col] = 2  # Mark as rotten
                        fresh_count -= 1
                        rotten_queue.append((adjacent_row, adjacent_col))
        
        return minutes_elapsed if fresh_count == 0 else -1
    
    def _is_valid_fresh_orange(self, grid: List[List[int]], row: int, col: int, rows: int, cols: int) -> bool:
        """
        Checks if the given position contains a fresh orange.
        
        Args:
            grid: The orange grid
            row: Row index to check
            col: Column index to check
            rows: Total number of rows
            cols: Total number of columns
            
        Returns:
            True if position is valid and contains fresh orange
        """
        return (0 <= row < rows and 
                0 <= col < cols and 
                grid[row][col] == 1)