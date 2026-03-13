from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Solves the N-Queens problem using backtracking.
        
        Args:
            n: Size of the chessboard (n x n)
            
        Returns:
            List of all valid N-Queens solutions, where each solution is
            represented as a list of strings showing queen positions
        """
        if n <= 0:
            return []
            
        all_solutions = []
        current_board = [-1] * n  # current_board[row] = column of queen in that row
        
        self._solve_queens_recursive(
            current_row=0,
            n=n,
            current_board=current_board,
            all_solutions=all_solutions
        )
        
        return all_solutions
    
    def _solve_queens_recursive(
        self, 
        current_row: int, 
        n: int, 
        current_board: List[int], 
        all_solutions: List[List[str]]
    ) -> None:
        """
        Recursively places queens on the board using backtracking.
        
        Args:
            current_row: The row we're currently trying to place a queen in
            n: Size of the chessboard
            current_board: Current state of queen placements
            all_solutions: List to collect all valid solutions
        """
        if current_row == n:
            # Found a complete solution
            board_representation = self._convert_board_to_strings(current_board, n)
            all_solutions.append(board_representation)
            return
        
        for column_position in range(n):
            if self._is_safe_position(current_row, column_position, current_board):
                current_board[current_row] = column_position  # Place queen
                
                self._solve_queens_recursive(
                    current_row + 1, 
                    n, 
                    current_board, 
                    all_solutions
                )
                
                current_board[current_row] = -1  # Backtrack
    
    def _is_safe_position(
        self, 
        target_row: int, 
        target_column: int, 
        current_board: List[int]
    ) -> bool:
        """
        Checks if placing a queen at (target_row, target_column) is safe.
        
        Args:
            target_row: Row to check
            target_column: Column to check
            current_board: Current queen placements
            
        Returns:
            True if the position is safe, False otherwise
        """
        for existing_row in range(target_row):
            existing_column = current_board[existing_row]
            
            if existing_column == -1:
                continue
                
            # Check column conflict
            if existing_column == target_column:
                return False
            
            # Check diagonal conflicts
            row_distance = target_row - existing_row
            column_distance = abs(target_column - existing_column)
            
            if row_distance == column_distance:  # Same diagonal
                return False
        
        return True
    
    def _convert_board_to_strings(self, board_state: List[int], n: int) -> List[str]:
        """
        Converts internal board representation to required string format.
        
        Args:
            board_state: Array where board_state[row] = column of queen
            n: Size of the chessboard
            
        Returns:
            List of strings representing the board with 'Q' for queens and '.' for empty
        """
        string_board = []
        
        for row_index in range(n):
            row_string = ['.'] * n
            queen_column = board_state[row_index]
            
            if queen_column != -1:
                row_string[queen_column] = 'Q'
            
            string_board.append(''.join(row_string))
        
        return string_board