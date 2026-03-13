from typing import List

class Solution:
    """Solution class for solving Sudoku puzzles using backtracking algorithm."""
    
    BOARD_SIZE: int = 9
    BOX_SIZE: int = 3
    EMPTY_CELL: str = '.'
    
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Solves a Sudoku puzzle by filling empty cells using backtracking.
        
        Args:
            board: 9x9 grid representing the Sudoku puzzle with '.' for empty cells
            
        Returns:
            None: Modifies the board in-place
        """
        self._solve_recursive(board)
    
    def _solve_recursive(self, board: List[List[str]]) -> bool:
        """
        Recursively solves the Sudoku puzzle using backtracking.
        
        Args:
            board: Current state of the Sudoku board
            
        Returns:
            bool: True if solution is found, False otherwise
        """
        empty_position = self._find_empty_cell(board)
        
        # Base case: no empty cells found, puzzle is solved
        if empty_position is None:
            return True
            
        current_row, current_col = empty_position
        
        # Try digits 1-9 in the empty cell
        for digit in range(1, self.BOARD_SIZE + 1):
            digit_str = str(digit)
            
            if self._is_valid_placement(board, current_row, current_col, digit_str):
                board[current_row][current_col] = digit_str  # Place digit
                
                # Recursively solve with this placement
                if self._solve_recursive(board):
                    return True
                
                # Backtrack: remove the digit if it doesn't lead to solution
                board[current_row][current_col] = self.EMPTY_CELL
        
        return False  # No valid digit found for this cell
    
    def _find_empty_cell(self, board: List[List[str]]) -> tuple[int, int] | None:
        """
        Finds the first empty cell in the Sudoku board.
        
        Args:
            board: Current state of the Sudoku board
            
        Returns:
            tuple[int, int] | None: Row and column indices of empty cell, or None if no empty cell
        """
        for row_index in range(self.BOARD_SIZE):
            for col_index in range(self.BOARD_SIZE):
                if board[row_index][col_index] == self.EMPTY_CELL:
                    return (row_index, col_index)
        return None
    
    def _is_valid_placement(self, board: List[List[str]], target_row: int, target_col: int, digit: str) -> bool:
        """
        Checks if placing a digit at the specified position is valid according to Sudoku rules.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row index where digit will be placed
            target_col: Column index where digit will be placed
            digit: Digit to be placed as string
            
        Returns:
            bool: True if placement is valid, False otherwise
        """
        return (self._is_valid_in_row(board, target_row, digit) and
                self._is_valid_in_column(board, target_col, digit) and
                self._is_valid_in_box(board, target_row, target_col, digit))
    
    def _is_valid_in_row(self, board: List[List[str]], target_row: int, digit: str) -> bool:
        """
        Checks if digit already exists in the specified row.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row index to check
            digit: Digit to check for as string
            
        Returns:
            bool: True if digit is not in row, False otherwise
        """
        return digit not in board[target_row]
    
    def _is_valid_in_column(self, board: List[List[str]], target_col: int, digit: str) -> bool:
        """
        Checks if digit already exists in the specified column.
        
        Args:
            board: Current state of the Sudoku board
            target_col: Column index to check
            digit: Digit to check for as string
            
        Returns:
            bool: True if digit is not in column, False otherwise
        """
        for row_index in range(self.BOARD_SIZE):
            if board[row_index][target_col] == digit:
                return False
        return True
    
    def _is_valid_in_box(self, board: List[List[str]], target_row: int, target_col: int, digit: str) -> bool:
        """
        Checks if digit already exists in the 3x3 box containing the target position.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row index of target position
            target_col: Column index of target position
            digit: Digit to check for as string
            
        Returns:
            bool: True if digit is not in the 3x3 box, False otherwise
        """
        # Calculate top-left corner of the 3x3 box
        box_start_row = (target_row // self.BOX_SIZE) * self.BOX_SIZE
        box_start_col = (target_col // self.BOX_SIZE) * self.BOX_SIZE
        
        # Check all cells in the 3x3 box
        for row_offset in range(self.BOX_SIZE):
            for col_offset in range(self.BOX_SIZE):
                current_row = box_start_row + row_offset
                current_col = box_start_col + col_offset
                if board[current_row][current_col] == digit:
                    return False
        
        return True