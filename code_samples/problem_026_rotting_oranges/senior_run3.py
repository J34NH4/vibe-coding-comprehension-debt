from typing import List, Deque
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Determines the minimum time for all fresh oranges to rot.
        
        Args:
            grid: 2D grid where 0=empty, 1=fresh orange, 2=rotten orange
            
        Returns:
            Minimum minutes for all oranges to rot, or -1 if impossible
        """
        if not grid or not grid[0]:
            return 0
            
        rows: int = len(grid)
        cols: int = len(grid[0])
        
        # Count fresh oranges and collect initial rotten positions
        fresh_count: int = 0
        rotten_queue: Deque[tuple] = deque()
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    fresh_count += 1
                elif grid[row][col] == 2:
                    rotten_queue.append((row, col))
        
        # If no fresh oranges, return 0
        if fresh_count == 0:
            return 0
        
        # If no rotten oranges but fresh exist, impossible
        if not rotten_queue:
            return -1
            
        minutes_elapsed: int = 0
        directions: List[tuple] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # BFS to spread rot
        while rotten_queue and fresh_count > 0:
            minutes_elapsed += 1
            current_level_size: int = len(rotten_queue)
            
            for _ in range(current_level_size):
                current_row, current_col = rotten_queue.popleft()
                
                # Check all 4 directions
                for delta_row, delta_col in directions:
                    neighbor_row: int = current_row + delta_row
                    neighbor_col: int = current_col + delta_col
                    
                    if self._is_valid_fresh_orange(grid, neighbor_row, neighbor_col, rows, cols):
                        grid[neighbor_row][neighbor_col] = 2  # Make it rotten
                        fresh_count -= 1
                        rotten_queue.append((neighbor_row, neighbor_col))
        
        return minutes_elapsed if fresh_count == 0 else -1
    
    def _is_valid_fresh_orange(self, grid: List[List[int]], row: int, col: int, 
                              total_rows: int, total_cols: int) -> bool:
        """
        Checks if the position contains a fresh orange within bounds.
        
        Args:
            grid: The orange grid
            row: Row index to check
            col: Column index to check
            total_rows: Total number of rows
            total_cols: Total number of columns
            
        Returns:
            True if position is valid and contains fresh orange
        """
        return (0 <= row < total_rows and 
                0 <= col < total_cols and 
                grid[row][col] == 1)