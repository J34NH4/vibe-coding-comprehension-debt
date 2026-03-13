from typing import List, Set, Tuple, Optional

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Solves a Sudoku puzzle in-place using backtracking algorithm.
        
        Args:
            board: 9x9 2D list representing the Sudoku board where '.' represents empty cells
            
        Returns:
            None: Modifies the board in-place
        """
        BOARD_SIZE = 9
        BOX_SIZE = 3
        EMPTY_CELL = '.'
        
        self._solve_sudoku_recursive(board, BOARD_SIZE, BOX_SIZE, EMPTY_CELL)
    
    def _solve_sudoku_recursive(self, board: List[List[str]], board_size: int, 
                               box_size: int, empty_cell: str) -> bool:
        """
        Recursively solves the Sudoku puzzle using backtracking.
        
        Args:
            board: The current state of the Sudoku board
            board_size: Size of the board (9 for standard Sudoku)
            box_size: Size of each box (3 for standard Sudoku)
            empty_cell: Character representing empty cells
            
        Returns:
            bool: True if puzzle is solved, False if current path is invalid
        """
        empty_position = self._find_next_empty_cell(board, board_size, empty_cell)
        
        if empty_position is None:  # No empty cells found, puzzle solved
            return True
        
        current_row, current_col = empty_position
        
        for candidate_digit in range(1, board_size + 1):
            digit_str = str(candidate_digit)
            
            if self._is_valid_placement(board, current_row, current_col, 
                                      digit_str, board_size, box_size):
                board[current_row][current_col] = digit_str  # Place digit
                
                if self._solve_sudoku_recursive(board, board_size, box_size, empty_cell):
                    return True  # Solution found in this branch
                
                board[current_row][current_col] = empty_cell  # Backtrack
        
        return False  # No valid digit found for this cell
    
    def _find_next_empty_cell(self, board: List[List[str]], board_size: int, 
                             empty_cell: str) -> Optional[Tuple[int, int]]:
        """
        Finds the next empty cell in the board using row-major order.
        
        Args:
            board: Current state of the Sudoku board
            board_size: Size of the board
            empty_cell: Character representing empty cells
            
        Returns:
            Optional[Tuple[int, int]]: Coordinates of next empty cell, or None if board is full
        """
        for row_index in range(board_size):
            for col_index in range(board_size):
                if board[row_index][col_index] == empty_cell:
                    return (row_index, col_index)
        return None
    
    def _is_valid_placement(self, board: List[List[str]], target_row: int, 
                           target_col: int, digit: str, board_size: int, 
                           box_size: int) -> bool:
        """
        Validates if placing a digit at the specified position follows Sudoku rules.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row index for digit placement
            target_col: Column index for digit placement
            digit: Digit to be placed
            board_size: Size of the board
            box_size: Size of each box
            
        Returns:
            bool: True if placement is valid, False otherwise
        """
        return (self._is_row_valid(board, target_row, digit, board_size) and
                self._is_column_valid(board, target_col, digit, board_size) and
                self._is_box_valid(board, target_row, target_col, digit, box_size))
    
    def _is_row_valid(self, board: List[List[str]], row_index: int, 
                     digit: str, board_size: int) -> bool:
        """
        Checks if digit already exists in the specified row.
        
        Args:
            board: Current state of the Sudoku board
            row_index: Row to check
            digit: Digit to validate
            board_size: Size of the board
            
        Returns:
            bool: True if digit is not in row, False otherwise
        """
        for col_index in range(board_size):
            if board[row_index][col_index] == digit:
                return False
        return True
    
    def _is_column_valid(self, board: List[List[str]], col_index: int, 
                        digit: str, board_size: int) -> bool:
        """
        Checks if digit already exists in the specified column.
        
        Args:
            board: Current state of the Sudoku board
            col_index: Column to check
            digit: Digit to validate
            board_size: Size of the board
            
        Returns:
            bool: True if digit is not in column, False otherwise
        """
        for row_index in range(board_size):
            if board[row_index][col_index] == digit:
                return False
        return True
    
    def _is_box_valid(self, board: List[List[str]], target_row: int, 
                     target_col: int, digit: str, box_size: int) -> bool:
        """
        Checks if digit already exists in the 3x3 box containing the target position.
        
        Args:
            board: Current state of the Sudoku board
            target_row: Row of target position
            target_col: Column of target position
            digit: Digit to validate
            box_size: Size of each box
            
        Returns:
            bool: True if digit is not in box, False otherwise
        """
        box_start_row = (target_row // box_size) * box_size
        box_start_col = (target_col // box_size) * box_size
        
        for row_offset in range(box_size):
            for col_offset in range(box_size):
                current_row = box_start_row + row_offset
                current_col = box_start_col + col_offset
                
                if board[current_row][current_col] == digit:
                    return False
        
        return True