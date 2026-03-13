from typing import List

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
            
        rows = len(matrix)
        columns = len(matrix[0])
        memoization_cache = {}  # Cache for storing computed path lengths
        
        def depth_first_search(current_row: int, current_column: int) -> int:
            """
            Perform DFS to find longest increasing path starting from given cell.
            
            Args:
                current_row: Row index of current cell
                current_column: Column index of current cell
                
            Returns:
                Length of longest increasing path from current cell
            """
            if (current_row, current_column) in memoization_cache:
                return memoization_cache[(current_row, current_column)]
            
            maximum_path_length = 1  # Current cell contributes 1 to path length
            current_value = matrix[current_row][current_column]
            
            # Explore all four directions
            for delta_row, delta_column in self._get_directions():
                next_row = current_row + delta_row
                next_column = current_column + delta_column
                
                if self._is_valid_cell(next_row, next_column, rows, columns):
                    next_value = matrix[next_row][next_column]
                    
                    # Only move to cells with strictly greater values
                    if next_value > current_value:
                        path_length_from_next = depth_first_search(next_row, next_column)
                        maximum_path_length = max(maximum_path_length, 1 + path_length_from_next)
            
            memoization_cache[(current_row, current_column)] = maximum_path_length
            return maximum_path_length
        
        longest_path = 0
        
        # Try starting from each cell in the matrix
        for row_index in range(rows):
            for column_index in range(columns):
                current_path_length = depth_first_search(row_index, column_index)
                longest_path = max(longest_path, current_path_length)
        
        return longest_path
    
    def _get_directions(self) -> List[tuple]:
        """
        Get the four possible movement directions (up, down, left, right).
        
        Returns:
            List of tuples representing direction vectors
        """
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def _is_valid_cell(self, row: int, column: int, total_rows: int, total_columns: int) -> bool:
        """
        Check if given coordinates represent a valid cell in the matrix.
        
        Args:
            row: Row index to validate
            column: Column index to validate
            total_rows: Total number of rows in matrix
            total_columns: Total number of columns in matrix
            
        Returns:
            Boolean indicating if coordinates are valid
        """
        return 0 <= row < total_rows and 0 <= column < total_columns