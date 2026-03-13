from typing import List, Tuple
from functools import lru_cache

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        """
        Find the length of the longest increasing path in a matrix.
        
        Args:
            matrix: 2D list of integers representing the matrix
            
        Returns:
            Integer representing the length of the longest increasing path
        """
        if not matrix or not matrix[0]:
            return 0
            
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        maximum_path_length = 0
        
        # Try starting from each cell in the matrix
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                current_path_length = self._find_longest_path_from_cell(row_index, col_index)
                maximum_path_length = max(maximum_path_length, current_path_length)
                
        return maximum_path_length
    
    @lru_cache(maxsize=None)
    def _find_longest_path_from_cell(self, row: int, col: int) -> int:
        """
        Find the longest increasing path starting from a specific cell using DFS with memoization.
        
        Args:
            row: Row index of the starting cell
            col: Column index of the starting cell
            
        Returns:
            Integer representing the longest path length from this cell
        """
        maximum_length_from_neighbors = 0
        current_cell_value = self.matrix[row][col]
        
        # Explore all four directions
        for delta_row, delta_col in self.directions:
            neighbor_row = row + delta_row
            neighbor_col = col + delta_col
            
            # Check if the neighbor is valid and has a greater value
            if self._is_valid_increasing_neighbor(neighbor_row, neighbor_col, current_cell_value):
                neighbor_path_length = self._find_longest_path_from_cell(neighbor_row, neighbor_col)
                maximum_length_from_neighbors = max(maximum_length_from_neighbors, neighbor_path_length)
        
        return maximum_length_from_neighbors + 1  # Include current cell in the path
    
    def _is_valid_increasing_neighbor(self, row: int, col: int, current_value: int) -> bool:
        """
        Check if a neighbor cell is valid and has a value greater than the current cell.
        
        Args:
            row: Row index of the neighbor cell
            col: Column index of the neighbor cell
            current_value: Value of the current cell
            
        Returns:
            Boolean indicating if the neighbor is valid for an increasing path
        """
        # Check bounds
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
            
        # Check if neighbor value is greater (for increasing path)
        return self.matrix[row][col] > current_value