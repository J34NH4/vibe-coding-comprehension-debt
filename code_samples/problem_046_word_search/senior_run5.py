from typing import List, Set, Tuple

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        Determines if a word exists in the character grid.
        
        Args:
            board: 2D grid of characters
            word: Target word to search for
            
        Returns:
            True if word exists in the grid, False otherwise
        """
        if not board or not board[0] or not word:
            return False
            
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = board
        self.word = word
        
        # Try starting from each cell in the board
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                if self._depth_first_search(row_index, col_index, 0, set()):
                    return True
        
        return False
    
    def _depth_first_search(self, row: int, col: int, word_index: int, visited_cells: Set[Tuple[int, int]]) -> bool:
        """
        Performs depth-first search to find word starting from given position.
        
        Args:
            row: Current row position
            col: Current column position
            word_index: Current index in the target word
            visited_cells: Set of already visited cell coordinates
            
        Returns:
            True if word can be formed from this position, False otherwise
        """
        # Check if we've found the complete word
        if word_index == len(self.word):
            return True
        
        # Check boundary conditions and character match
        if (row < 0 or row >= self.rows or 
            col < 0 or col >= self.cols or
            (row, col) in visited_cells or
            self.board[row][col] != self.word[word_index]):
            return False
        
        # Mark current cell as visited
        visited_cells.add((row, col))
        
        # Define possible movement directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Explore all adjacent cells
        for delta_row, delta_col in directions:
            next_row = row + delta_row
            next_col = col + delta_col
            
            if self._depth_first_search(next_row, next_col, word_index + 1, visited_cells):
                visited_cells.remove((row, col))  # Backtrack
                return True
        
        # Backtrack: remove current cell from visited set
        visited_cells.remove((row, col))
        return False