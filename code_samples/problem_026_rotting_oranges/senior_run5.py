from collections import deque
from typing import List, Tuple, Set

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Determines the minimum time for all oranges to rot using BFS.
        
        Args:
            grid: 2D list where 0=empty, 1=fresh orange, 2=rotten orange
            
        Returns:
            Minutes until all oranges rot, or -1 if impossible
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
                    rotten_queue.append((row, col, 0))  # row, col, time
        
        # No fresh oranges to rot
        if fresh_count == 0:
            return 0
            
        return self._bfs_rot_oranges(grid, rotten_queue, fresh_count, rows, cols)
    
    def _bfs_rot_oranges(self, grid: List[List[int]], rotten_queue: deque, 
                        fresh_count: int, rows: int, cols: int) -> int:
        """
        Performs BFS to rot adjacent fresh oranges level by level.
        
        Args:
            grid: The orange grid
            rotten_queue: Queue of initially rotten oranges with timestamps
            fresh_count: Count of fresh oranges remaining
            rows: Number of rows in grid
            cols: Number of columns in grid
            
        Returns:
            Minutes taken to rot all oranges, or -1 if impossible
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        max_time = 0
        
        while rotten_queue:
            current_row, current_col, current_time = rotten_queue.popleft()
            max_time = max(max_time, current_time)
            
            # Check all 4 adjacent cells
            for delta_row, delta_col in directions:
                next_row = current_row + delta_row
                next_col = current_col + delta_col
                
                if self._is_valid_fresh_orange(grid, next_row, next_col, rows, cols):
                    grid[next_row][next_col] = 2  # Rot the orange
                    fresh_count -= 1
                    rotten_queue.append((next_row, next_col, current_time + 1))
        
        return max_time if fresh_count == 0 else -1
    
    def _is_valid_fresh_orange(self, grid: List[List[int]], row: int, col: int, 
                              rows: int, cols: int) -> bool:
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