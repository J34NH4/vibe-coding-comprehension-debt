from typing import List, Set, Tuple, Optional

class Solution:
    """Solution for LeetCode #37: Sudoku Solver."""
    
    BOARD_SIZE: int = 9
    SUBGRID_SIZE: int = 3
    EMPTY_CELL: str = '.'
    
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Solve a Sudoku puzzle by filling the empty cells.
        
        Args:
            board: 9x9 grid representing the Sudoku puzzle with '.' for empty cells
            
        Returns:
            None: Modifies the board in-place
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
        empty_position = self._find_next_empty_cell(board)
        
        if empty_position is None:  # No empty cells found - puzzle solved
            return True
            
        row_index, column_index = empty_position
        
        for candidate_digit in range(1, self.BOARD_SIZE + 1):
            digit_string = str(candidate_digit)
            
            if self._is_valid_placement(board, row_index, column_index, digit_string):
                board[row_index][column_index] = digit_string  # Make move
                
                if self._solve_sudoku_recursive(board):  # Recurse
                    return True
                    
                board[row_index][column_index] = self.EMPTY_CELL  # Backtrack
        
        return False
    
    def _find_next_empty_cell(self, board: List[List[str]]) -> Optional[Tuple[int, int]]:
        """
        Find the next empty cell in the board.
        
        Args:
            board: Current state of the Sudoku board
            
        Returns:
            Optional[Tuple[int, int]]: Position of next empty cell or None if board is full
        """
        for row_index in range(self.BOARD_SIZE):
            for column_index in range(self.BOARD_SIZE):
                if board[row_index][column_index] == self.EMPTY_CELL:
                    return (row_index, column_index)
        return None
    
    def _is_valid_placement(self, board: List[List[str]], row_index: int, 
                           column_index: int, digit: str) -> bool:
        """
        Check if placing a digit at the given position is valid.
        
        Args:
            board: Current state of the Sudoku board
            row_index: Row position to check
            column_index: Column position to check
            digit: Digit to place
            
        Returns:
            bool: True if placement is valid, False otherwise
        """
        return (self._is_valid_in_row(board, row_index, digit) and
                self._is_valid_in_column(board, column_index, digit) and
                self._is_valid_in_subgrid(board, row_index, column_index, digit))
    
    def _is_valid_in_row(self, board: List[List[str]], row_index: int, digit: str) -> bool:
        """
        Check if digit is valid in the specified row.
        
        Args:
            board: Current state of the Sudoku board
            row_index: Row to check
            digit: Digit to validate
            
        Returns:
            bool: True if digit doesn't exist in row, False otherwise
        """
        return digit not in board[row_index]
    
    def _is_valid_in_column(self, board: List[List[str]], column_index: int, digit: str) -> bool:
        """
        Check if digit is valid in the specified column.
        
        Args:
            board: Current state of the Sudoku board
            column_index: Column to check
            digit: Digit to validate
            
        Returns:
            bool: True if digit doesn't exist in column, False otherwise
        """
        for row_index in range(self.BOARD_SIZE):
            if board[row_index][column_index] == digit:
                return False
        return True
    
    def _is_valid_in_subgrid(self, board: List[List[str]], row_index: int, 
                            column_index: int, digit: str) -> bool:
        """
        Check if digit is valid in the 3x3 subgrid containing the given position.
        
        Args:
            board: Current state of the Sudoku board
            row_index: Row position
            column_index: Column position
            digit: Digit to validate
            
        Returns:
            bool: True if digit doesn't exist in subgrid, False otherwise
        """
        subgrid_start_row = (row_index // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        subgrid_start_column = (column_index // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        
        for current_row in range(subgrid_start_row, subgrid_start_row + self.SUBGRID_SIZE):
            for current_column in range(subgrid_start_column, subgrid_start_column + self.SUBGRID_SIZE):
                if board[current_row][current_column] == digit:
                    return False
        return True