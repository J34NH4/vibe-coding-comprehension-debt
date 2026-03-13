from typing import List, Tuple, Set
from functools import lru_cache

class Solution:
    """Solution for finding the longest increasing path in a matrix."""
    
    DIRECTIONS: List[Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        """
        Find the length of the longest increasing path in the matrix.
        
        Args:
            matrix: 2D list of integers representing the matrix
            
        Returns:
            int: Length of the longest increasing path
            
        Raises:
            ValueError: If matrix is empty or invalid
        """
        if not matrix or not matrix[0]:
            raise ValueError("Matrix cannot be empty")
            
        self.matrix_rows = len(matrix)
        self.matrix_cols = len(matrix[0])
        self.matrix = matrix
        
        maximum_path_length = 0
        
        # Try starting from each cell in the matrix
        for current_row in range(self.matrix_rows):
            for current_col in range(self.matrix_cols):
                current_path_length = self._find_longest_path_from_cell(current_row, current_col)
                maximum_path_length = max(maximum_path_length, current_path_length)
                
        return maximum_path_length
    
    @lru_cache(maxsize=None)
    def _find_longest_path_from_cell(self, start_row: int, start_col: int) -> int:
        """
        Find the longest increasing path starting from a specific cell using DFS with memoization.
        
        Args:
            start_row: Starting row position
            start_col: Starting column position
            
        Returns:
            int: Length of longest increasing path from this cell
        """
        maximum_length_from_neighbors = 0
        current_cell_value = self.matrix[start_row][start_col]
        
        # Explore all four directions
        for row_delta, col_delta in self.DIRECTIONS:
            neighbor_row = start_row + row_delta
            neighbor_col = start_col + col_delta
            
            if self._is_valid_next_cell(neighbor_row, neighbor_col, current_cell_value):
                neighbor_path_length = self._find_longest_path_from_cell(neighbor_row, neighbor_col)
                maximum_length_from_neighbors = max(maximum_length_from_neighbors, neighbor_path_length)
        
        # Current cell contributes 1 to the path length
        return maximum_length_from_neighbors + 1
    
    def _is_valid_next_cell(self, target_row: int, target_col: int, current_value: int) -> bool:
        """
        Check if a cell is valid for the increasing path.
        
        Args:
            target_row: Row of the target cell
            target_col: Column of the target cell
            current_value: Value of the current cell
            
        Returns:
            bool: True if the target cell is valid for the increasing path
        """
        # Check bounds
        if target_row < 0 or target_row >= self.matrix_rows:
            return False
        if target_col < 0 or target_col >= self.matrix_cols:
            return False
            
        # Check if value is strictly increasing
        target_value = self.matrix[target_row][target_col]
        return target_value > current_value