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
            
        num_rows = len(matrix)
        num_cols = len(matrix[0])
        memoization_cache = {}  # Cache for dynamic programming
        
        def _depth_first_search(current_row: int, current_col: int) -> int:
            """
            Perform DFS to find longest increasing path starting from given position.
            
            Args:
                current_row: Current row position in matrix
                current_col: Current column position in matrix
                
            Returns:
                Length of longest increasing path from this position
            """
            if (current_row, current_col) in memoization_cache:
                return memoization_cache[(current_row, current_col)]
            
            max_path_length = 1  # At minimum, path includes current cell
            current_value = matrix[current_row][current_col]
            
            # Check all four directions
            for delta_row, delta_col in DIRECTIONS:
                next_row = current_row + delta_row
                next_col = current_col + delta_col
                
                # Validate bounds and increasing condition
                if (self._is_valid_position(next_row, next_col, num_rows, num_cols) and
                    matrix[next_row][next_col] > current_value):
                    
                    path_from_next = _depth_first_search(next_row, next_col)
                    max_path_length = max(max_path_length, 1 + path_from_next)
            
            memoization_cache[(current_row, current_col)] = max_path_length
            return max_path_length
        
        longest_path = 0
        
        # Try starting from each cell in the matrix
        for row_index in range(num_rows):
            for col_index in range(num_cols):
                current_path_length = _depth_first_search(row_index, col_index)
                longest_path = max(longest_path, current_path_length)
        
        return longest_path
    
    def _is_valid_position(self, row: int, col: int, num_rows: int, num_cols: int) -> bool:
        """
        Check if given position is within matrix bounds.
        
        Args:
            row: Row index to check
            col: Column index to check
            num_rows: Total number of rows in matrix
            num_cols: Total number of columns in matrix
            
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= row < num_rows and 0 <= col < num_cols

# Direction vectors for up, down, left, right movement
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]