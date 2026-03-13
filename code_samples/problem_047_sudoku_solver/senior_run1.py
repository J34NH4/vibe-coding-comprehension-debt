from typing import List, Tuple, Set

class Solution:
    """Solution class for solving Sudoku puzzles using backtracking algorithm."""
    
    BOARD_SIZE = 9
    SUBGRID_SIZE = 3
    EMPTY_CELL = '.'
    
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Solve a Sudoku puzzle by filling the empty cells.
        
        Args:
            board: 9x9 grid representing the Sudoku puzzle, modified in-place
            
        Returns:
            None: The board is modified in-place
        """
        if not board or len(board) != self.BOARD_SIZE:
            raise ValueError("Invalid board dimensions")
            
        self._solve_sudoku_recursive(board)
    
    def _solve_sudoku_recursive(self, board: List[List[str]]) -> bool:
        """
        Recursively solve the Sudoku puzzle using backtracking.
        
        Args:
            board: Current state of the Sudoku board
            
        Returns:
            bool: True if puzzle is solved, False otherwise
        """
        empty_cell_position = self._find_next_empty_cell(board)
        
        # Base case: no empty cells found, puzzle is solved
        if empty_cell_position is None:
            return True
            
        current_row, current_column = empty_cell_position
        
        # Try digits 1-9 for the empty cell
        for candidate_digit in range(1, 10):
            digit_string = str(candidate_digit)
            
            if self._is_valid_placement(board, current_row, current_column, digit_string):
                board[current_row][current_column] = digit_string  # Place digit
                
                # Recursively solve remaining puzzle
                if self._solve_sudoku_recursive(board):
                    return True
                    
                # Backtrack: remove digit if it doesn't lead to solution
                board[current_row][current_column] = self.EMPTY_CELL
        
        return False  # No valid digit found for this cell
    
    def _find_next_empty_cell(self, board: List[List[str]]) -> Tuple[int, int] | None:
        """
        Find the next empty cell in the board.
        
        Args:
            board: Current state of the Sudoku board
            
        Returns:
            Tuple[int, int] | None: Row and column indices of empty cell, or None if none found
        """
        for row_index in range(self.BOARD_SIZE):
            for column_index in range(self.BOARD_SIZE):
                if board[row_index][column_index] == self.EMPTY_CELL:
                    return (row_index, column_index)
        return None
    
    def _is_valid_placement(self, board: List[List[str]], target_row: int, 
                          target_column: int, candidate_digit: str) -> bool:
        """
        Check if placing a digit at the specified position is valid.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row index for placement
            target_column: Column index for placement
            candidate_digit: Digit to be placed
            
        Returns:
            bool: True if placement is valid, False otherwise
        """
        return (self._is_valid_in_row(board, target_row, candidate_digit) and
                self._is_valid_in_column(board, target_column, candidate_digit) and
                self._is_valid_in_subgrid(board, target_row, target_column, candidate_digit))
    
    def _is_valid_in_row(self, board: List[List[str]], target_row: int, 
                        candidate_digit: str) -> bool:
        """
        Check if digit is valid in the specified row.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row index to check
            candidate_digit: Digit to validate
            
        Returns:
            bool: True if digit is not already in row, False otherwise
        """
        for column_index in range(self.BOARD_SIZE):
            if board[target_row][column_index] == candidate_digit:
                return False
        return True
    
    def _is_valid_in_column(self, board: List[List[str]], target_column: int, 
                           candidate_digit: str) -> bool:
        """
        Check if digit is valid in the specified column.
        
        Args:
            board: Current state of the Sudoku board
            target_column: Column index to check
            candidate_digit: Digit to validate
            
        Returns:
            bool: True if digit is not already in column, False otherwise
        """
        for row_index in range(self.BOARD_SIZE):
            if board[row_index][target_column] == candidate_digit:
                return False
        return True
    
    def _is_valid_in_subgrid(self, board: List[List[str]], target_row: int, 
                            target_column: int, candidate_digit: str) -> bool:
        """
        Check if digit is valid in the 3x3 subgrid containing the target position.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row index of target position
            target_column: Column index of target position
            candidate_digit: Digit to validate
            
        Returns:
            bool: True if digit is not already in subgrid, False otherwise
        """
        # Calculate top-left corner of the 3x3 subgrid
        subgrid_start_row = (target_row // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        subgrid_start_column = (target_column // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        
        # Check all cells in the 3x3 subgrid
        for row_offset in range(self.SUBGRID_SIZE):
            for column_offset in range(self.SUBGRID_SIZE):
                current_row = subgrid_start_row + row_offset
                current_column = subgrid_start_column + column_offset
                
                if board[current_row][current_column] == candidate_digit:
                    return False
                    
        return True