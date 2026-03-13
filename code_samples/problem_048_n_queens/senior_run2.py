from typing import List


class Solution:
    """Solution for the N-Queens problem."""
    
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Solve the N-Queens problem using backtracking.
        
        Args:
            n: Size of the chessboard (n x n)
            
        Returns:
            List of all valid board configurations as string representations
        """
        if n <= 0:
            return []
            
        solutions = []
        current_board = [-1] * n  # current_board[row] = column position of queen
        
        self._place_queens(n, 0, current_board, solutions)
        return solutions
    
    def _place_queens(self, board_size: int, current_row: int, 
                     current_board: List[int], solutions: List[List[str]]) -> None:
        """
        Recursively place queens on the board using backtracking.
        
        Args:
            board_size: Size of the board
            current_row: Current row being processed
            current_board: Current state of queen positions
            solutions: List to store all valid solutions
        """
        if current_row == board_size:
            # All queens placed successfully
            board_representation = self._convert_to_board_strings(current_board, board_size)
            solutions.append(board_representation)
            return
        
        for column_position in range(board_size):
            if self._is_safe_position(current_board, current_row, column_position):
                current_board[current_row] = column_position  # Place queen
                self._place_queens(board_size, current_row + 1, current_board, solutions)
                current_board[current_row] = -1  # Backtrack
    
    def _is_safe_position(self, current_board: List[int], target_row: int, 
                         target_column: int) -> bool:
        """
        Check if placing a queen at the given position is safe.
        
        Args:
            current_board: Current state of queen positions
            target_row: Row to check
            target_column: Column to check
            
        Returns:
            True if position is safe, False otherwise
        """
        for previous_row in range(target_row):
            previous_column = current_board[previous_row]
            
            if previous_column == -1:  # No queen placed in this row yet
                continue
                
            # Check column conflict
            if previous_column == target_column:
                return False
                
            # Check diagonal conflicts
            row_difference = abs(target_row - previous_row)
            column_difference = abs(target_column - previous_column)
            
            if row_difference == column_difference:  # Same diagonal
                return False
        
        return True
    
    def _convert_to_board_strings(self, queen_positions: List[int], 
                                 board_size: int) -> List[str]:
        """
        Convert queen positions to board string representation.
        
        Args:
            queen_positions: List where index is row and value is column of queen
            board_size: Size of the board
            
        Returns:
            List of strings representing the board configuration
        """
        board_strings = []
        
        for row_index in range(board_size):
            row_string = ['.' for _ in range(board_size)]
            queen_column = queen_positions[row_index]
            
            if queen_column != -1:  # Queen is placed in this row
                row_string[queen_column] = 'Q'
                
            board_strings.append(''.join(row_string))
        
        return board_strings