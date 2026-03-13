from typing import List, Tuple
from functools import lru_cache

class Solution:
    """Solution for finding the longest increasing path in a matrix."""
    
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        """
        Find the length of the longest increasing path in the matrix.
        
        Args:
            matrix: 2D list of integers representing the matrix
            
        Returns:
            Integer representing the length of the longest increasing path
            
        Raises:
            ValueError: If matrix is empty or invalid
        """
        if not matrix or not matrix[0]:
            return 0
            
        self._matrix = matrix
        self._rows = len(matrix)
        self._columns = len(matrix[0])
        self._directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        maximum_path_length = 0
        
        # Try starting from each cell in the matrix
        for current_row in range(self._rows):
            for current_column in range(self._columns):
                path_length = self._find_longest_path_from_cell(current_row, current_column)
                maximum_path_length = max(maximum_path_length, path_length)
                
        return maximum_path_length
    
    @lru_cache(maxsize=None)
    def _find_longest_path_from_cell(self, row: int, column: int) -> int:
        """
        Find the longest increasing path starting from a specific cell using DFS with memoization.
        
        Args:
            row: Row index of the starting cell
            column: Column index of the starting cell
            
        Returns:
            Integer representing the longest path length from this cell
        """
        current_value = self._matrix[row][column]
        maximum_length_from_neighbors = 0
        
        # Check all four directions
        for delta_row, delta_column in self._directions:
            neighbor_row = row + delta_row
            neighbor_column = column + delta_column
            
            # Validate neighbor coordinates and check if value is increasing
            if self._is_valid_increasing_neighbor(neighbor_row, neighbor_column, current_value):
                neighbor_path_length = self._find_longest_path_from_cell(neighbor_row, neighbor_column)
                maximum_length_from_neighbors = max(maximum_length_from_neighbors, neighbor_path_length)
        
        return maximum_length_from_neighbors + 1  # Include current cell
    
    def _is_valid_increasing_neighbor(self, row: int, column: int, current_value: int) -> bool:
        """
        Check if the neighbor cell is valid and has a greater value.
        
        Args:
            row: Row index of the neighbor cell
            column: Column index of the neighbor cell
            current_value: Value of the current cell
            
        Returns:
            Boolean indicating if the neighbor is valid and increasing
        """
        # Check bounds
        if row < 0 or row >= self._rows or column < 0 or column >= self._columns:
            return False
            
        # Check if neighbor value is greater than current value
        return self._matrix[row][column] > current_value