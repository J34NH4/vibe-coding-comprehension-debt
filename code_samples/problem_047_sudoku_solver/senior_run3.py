from typing import List, Set, Tuple, Optional

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Solve a Sudoku puzzle by filling the empty cells.
        
        Args:
            board: 9x9 grid with digits 1-9 and '.' for empty cells
            
        Returns:
            None: Modifies board in-place
        """
        BOARD_SIZE = 9
        BOX_SIZE = 3
        EMPTY_CELL = '.'
        
        def is_valid_placement(row: int, col: int, digit: str) -> bool:
            """
            Check if placing digit at (row, col) is valid.
            
            Args:
                row: Row index (0-8)
                col: Column index (0-8) 
                digit: Digit to place ('1'-'9')
                
            Returns:
                True if placement is valid, False otherwise
            """
            # Check row constraint
            for column_index in range(BOARD_SIZE):
                if board[row][column_index] == digit:
                    return False
            
            # Check column constraint
            for row_index in range(BOARD_SIZE):
                if board[row_index][col] == digit:
                    return False
            
            # Check 3x3 box constraint
            box_start_row = (row // BOX_SIZE) * BOX_SIZE
            box_start_col = (col // BOX_SIZE) * BOX_SIZE
            
            for box_row in range(box_start_row, box_start_row + BOX_SIZE):
                for box_col in range(box_start_col, box_start_col + BOX_SIZE):
                    if board[box_row][box_col] == digit:
                        return False
            
            return True
        
        def find_next_empty_cell() -> Optional[Tuple[int, int]]:
            """
            Find the next empty cell in the board.
            
            Returns:
                Tuple of (row, col) for next empty cell, or None if board is complete
            """
            for row_index in range(BOARD_SIZE):
                for col_index in range(BOARD_SIZE):
                    if board[row_index][col_index] == EMPTY_CELL:
                        return (row_index, col_index)
            return None
        
        def solve_recursive() -> bool:
            """
            Recursively solve the Sudoku using backtracking.
            
            Returns:
                True if solution found, False if no solution exists
            """
            empty_cell_position = find_next_empty_cell()
            
            # Base case: no empty cells means puzzle is solved
            if empty_cell_position is None:
                return True
            
            current_row, current_col = empty_cell_position
            
            # Try each digit 1-9
            for digit_candidate in '123456789':
                if is_valid_placement(current_row, current_col, digit_candidate):
                    # Place digit and recurse
                    board[current_row][current_col] = digit_candidate
                    
                    if solve_recursive():
                        return True
                    
                    # Backtrack: remove digit if it doesn't lead to solution
                    board[current_row][current_col] = EMPTY_CELL
            
            return False
        
        # Validate input board dimensions
        if len(board) != BOARD_SIZE or any(len(row) != BOARD_SIZE for row in board):
            raise ValueError("Invalid board dimensions")
        
        # Start solving from the first empty cell
        solve_recursive()