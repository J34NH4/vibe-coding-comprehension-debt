from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Solve the N-Queens problem using backtracking.
        
        Args:
            n: Size of the chessboard (n x n)
            
        Returns:
            List of all valid solutions, where each solution is represented
            as a list of strings showing queen positions
        """
        if n <= 0:
            return []
            
        all_solutions = []
        current_board = [-1] * n  # current_board[row] = column of queen in that row
        
        self._solve_n_queens_recursive(n, 0, current_board, all_solutions)
        return all_solutions
    
    def _solve_n_queens_recursive(
        self, 
        board_size: int, 
        current_row: int, 
        current_board: List[int], 
        all_solutions: List[List[str]]
    ) -> None:
        """
        Recursively solve N-Queens using backtracking.
        
        Args:
            board_size: Size of the chessboard
            current_row: Current row being processed
            current_board: Current state of queen positions
            all_solutions: List to store all valid solutions
        """
        if current_row == board_size:
            # Found a complete solution
            board_representation = self._convert_to_board_strings(current_board, board_size)
            all_solutions.append(board_representation)
            return
        
        for column_position in range(board_size):
            if self._is_safe_position(current_board, current_row, column_position):
                current_board[current_row] = column_position  # Place queen
                self._solve_n_queens_recursive(board_size, current_row + 1, current_board, all_solutions)
                current_board[current_row] = -1  # Backtrack
    
    def _is_safe_position(self, current_board: List[int], target_row: int, target_column: int) -> bool:
        """
        Check if placing a queen at (target_row, target_column) is safe.
        
        Args:
            current_board: Current state of queen positions
            target_row: Row where we want to place the queen
            target_column: Column where we want to place the queen
            
        Returns:
            True if the position is safe, False otherwise
        """
        for existing_row in range(target_row):
            existing_column = current_board[existing_row]
            
            if existing_column == -1:  # No queen placed in this row yet
                continue
                
            # Check column conflict
            if existing_column == target_column:
                return False
                
            # Check diagonal conflicts
            row_difference = abs(existing_row - target_row)
            column_difference = abs(existing_column - target_column)
            if row_difference == column_difference:  # Same diagonal
                return False
        
        return True
    
    def _convert_to_board_strings(self, queen_positions: List[int], board_size: int) -> List[str]:
        """
        Convert queen positions array to board string representation.
        
        Args:
            queen_positions: Array where queen_positions[row] = column of queen
            board_size: Size of the chessboard
            
        Returns:
            List of strings representing the board state
        """
        board_strings = []
        
        for row_index in range(board_size):
            row_string = ""
            queen_column = queen_positions[row_index]
            
            for column_index in range(board_size):
                if column_index == queen_column:
                    row_string += "Q"  # Queen position
                else:
                    row_string += "."  # Empty position
            
            board_strings.append(row_string)
        
        return board_strings