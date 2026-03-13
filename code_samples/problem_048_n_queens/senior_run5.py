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
        current_board = [-1] * n  # current_board[row] = col position of queen
        
        self._solve_queens_recursive(
            current_row=0,
            current_board=current_board,
            all_solutions=all_solutions,
            board_size=n
        )
        
        return all_solutions
    
    def _solve_queens_recursive(
        self,
        current_row: int,
        current_board: List[int],
        all_solutions: List[List[str]],
        board_size: int
    ) -> None:
        """
        Recursively place queens on the board using backtracking.
        
        Args:
            current_row: Current row being processed
            current_board: Current state of queen positions
            all_solutions: List to store all valid solutions
            board_size: Size of the chessboard
        """
        if current_row == board_size:
            # All queens placed successfully, convert to required format
            board_representation = self._convert_board_to_strings(
                current_board, board_size
            )
            all_solutions.append(board_representation)
            return
        
        for candidate_column in range(board_size):
            if self._is_safe_position(current_row, candidate_column, current_board):
                # Place queen at this position
                current_board[current_row] = candidate_column
                
                # Recursively solve for next row
                self._solve_queens_recursive(
                    current_row + 1,
                    current_board,
                    all_solutions,
                    board_size
                )
                
                # Backtrack - remove queen from current position
                current_board[current_row] = -1
    
    def _is_safe_position(
        self,
        target_row: int,
        target_column: int,
        current_board: List[int]
    ) -> bool:
        """
        Check if placing a queen at (target_row, target_column) is safe.
        
        Args:
            target_row: Row where we want to place the queen
            target_column: Column where we want to place the queen
            current_board: Current state of queen positions
            
        Returns:
            True if the position is safe, False otherwise
        """
        for existing_row in range(target_row):
            existing_column = current_board[existing_row]
            
            # Check if queens are in same column
            if existing_column == target_column:
                return False
            
            # Check diagonal conflicts
            row_difference = abs(target_row - existing_row)
            column_difference = abs(target_column - existing_column)
            
            if row_difference == column_difference:  # Same diagonal
                return False
        
        return True
    
    def _convert_board_to_strings(
        self,
        queen_positions: List[int],
        board_size: int
    ) -> List[str]:
        """
        Convert internal board representation to required string format.
        
        Args:
            queen_positions: Array where queen_positions[row] = column
            board_size: Size of the chessboard
            
        Returns:
            List of strings representing the board with queens placed
        """
        QUEEN_SYMBOL = 'Q'
        EMPTY_SYMBOL = '.'
        
        board_strings = []
        
        for row_index in range(board_size):
            row_string = ''
            queen_column = queen_positions[row_index]
            
            for column_index in range(board_size):
                if column_index == queen_column:
                    row_string += QUEEN_SYMBOL
                else:
                    row_string += EMPTY_SYMBOL
            
            board_strings.append(row_string)
        
        return board_strings