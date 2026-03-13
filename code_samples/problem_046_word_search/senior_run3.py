from typing import List, Set, Tuple


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        Determines if a word exists in the character board using DFS backtracking.
        
        Args:
            board: 2D grid of characters
            word: Target word to search for
            
        Returns:
            True if word exists in board, False otherwise
        """
        if not board or not board[0] or not word:
            return False
            
        board_rows = len(board)
        board_cols = len(board[0])
        
        # Try starting DFS from each cell
        for start_row in range(board_rows):
            for start_col in range(board_cols):
                if self._dfs_search(board, word, start_row, start_col, 0, set()):
                    return True
        
        return False
    
    def _dfs_search(
        self, 
        board: List[List[str]], 
        target_word: str, 
        current_row: int, 
        current_col: int, 
        word_index: int, 
        visited_cells: Set[Tuple[int, int]]
    ) -> bool:
        """
        Performs depth-first search to find target word starting from given position.
        
        Args:
            board: 2D character grid
            target_word: Word to search for
            current_row: Current row position
            current_col: Current column position
            word_index: Current index in target word
            visited_cells: Set of already visited cell coordinates
            
        Returns:
            True if word can be formed from current position, False otherwise
        """
        # Base case: found complete word
        if word_index == len(target_word):
            return True
        
        # Check bounds and cell validity
        if not self._is_valid_cell(board, current_row, current_col, visited_cells):
            return False
        
        # Check character match
        if board[current_row][current_col] != target_word[word_index]:
            return False
        
        # Mark current cell as visited
        current_position = (current_row, current_col)
        visited_cells.add(current_position)
        
        # Explore all four directions
        direction_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for row_offset, col_offset in direction_offsets:
            next_row = current_row + row_offset
            next_col = current_col + col_offset
            
            if self._dfs_search(board, target_word, next_row, next_col, word_index + 1, visited_cells):
                visited_cells.remove(current_position)  # backtrack
                return True
        
        # Backtrack: remove current cell from visited set
        visited_cells.remove(current_position)
        return False
    
    def _is_valid_cell(
        self, 
        board: List[List[str]], 
        row: int, 
        col: int, 
        visited_cells: Set[Tuple[int, int]]
    ) -> bool:
        """
        Checks if given cell coordinates are valid and unvisited.
        
        Args:
            board: 2D character grid
            row: Row coordinate to check
            col: Column coordinate to check
            visited_cells: Set of already visited coordinates
            
        Returns:
            True if cell is valid and unvisited, False otherwise
        """
        return (
            0 <= row < len(board) and 
            0 <= col < len(board[0]) and 
            (row, col) not in visited_cells
        )