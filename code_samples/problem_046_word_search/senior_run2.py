from typing import List, Set, Tuple

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        Determines if a word exists in the character board using DFS.
        
        Args:
            board: 2D list of characters representing the grid
            word: Target word to search for
            
        Returns:
            True if word exists in the board, False otherwise
        """
        if not board or not board[0] or not word:
            return False
            
        self.board_rows = len(board)
        self.board_cols = len(board[0])
        
        # Try starting DFS from each cell in the board
        for row_index in range(self.board_rows):
            for col_index in range(self.board_cols):
                if self._depth_first_search(board, word, row_index, col_index, 0, set()):
                    return True
        
        return False
    
    def _depth_first_search(
        self, 
        board: List[List[str]], 
        target_word: str, 
        current_row: int, 
        current_col: int, 
        word_index: int, 
        visited_cells: Set[Tuple[int, int]]
    ) -> bool:
        """
        Performs depth-first search to find the target word starting from current position.
        
        Args:
            board: 2D character grid
            target_word: Word being searched for
            current_row: Current row position in board
            current_col: Current column position in board
            word_index: Current index in the target word
            visited_cells: Set of already visited cell coordinates
            
        Returns:
            True if word can be formed from current position, False otherwise
        """
        # Base case: found complete word
        if word_index == len(target_word):
            return True
        
        # Check bounds and visited status
        if (current_row < 0 or current_row >= self.board_rows or 
            current_col < 0 or current_col >= self.board_cols or
            (current_row, current_col) in visited_cells):
            return False
        
        # Check if current character matches target
        current_character = board[current_row][current_col]
        if current_character != target_word[word_index]:
            return False
        
        # Mark current cell as visited
        visited_cells.add((current_row, current_col))
        
        # Define possible directions: up, down, left, right
        direction_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Explore all adjacent cells
        for row_offset, col_offset in direction_offsets:
            next_row = current_row + row_offset
            next_col = current_col + col_offset
            
            if self._depth_first_search(
                board, target_word, next_row, next_col, 
                word_index + 1, visited_cells
            ):
                visited_cells.remove((current_row, current_col))  # Backtrack
                return True
        
        # Backtrack: remove current cell from visited set
        visited_cells.remove((current_row, current_col))
        return False