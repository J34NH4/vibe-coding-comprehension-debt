from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        Determines if a word exists in the character board using DFS.
        
        Args:
            board: 2D grid of characters
            word: Target word to search for
            
        Returns:
            True if word exists in the board, False otherwise
        """
        if not board or not board[0] or not word:
            return False
            
        rows = len(board)
        cols = len(board[0])
        
        def _dfs_search(row: int, col: int, word_index: int, visited_cells: set) -> bool:
            """
            Performs depth-first search to find word starting from given position.
            
            Args:
                row: Current row position
                col: Current column position
                word_index: Current index in the target word
                visited_cells: Set of already visited cell coordinates
                
            Returns:
                True if word can be formed from current position
            """
            # Base case: found complete word
            if word_index == len(word):
                return True
                
            # Check bounds and cell availability
            if (row < 0 or row >= rows or col < 0 or col >= cols or 
                (row, col) in visited_cells or 
                board[row][col] != word[word_index]):
                return False
                
            # Mark current cell as visited
            visited_cells.add((row, col))
            
            # Explore all four directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
            for delta_row, delta_col in directions:
                next_row = row + delta_row
                next_col = col + delta_col
                
                if _dfs_search(next_row, next_col, word_index + 1, visited_cells):
                    visited_cells.remove((row, col))  # backtrack
                    return True
                    
            # Backtrack: remove current cell from visited set
            visited_cells.remove((row, col))
            return False
        
        # Try starting from each cell in the board
        for start_row in range(rows):
            for start_col in range(cols):
                if board[start_row][start_col] == word[0]:  # optimization: check first character
                    if _dfs_search(start_row, start_col, 0, set()):
                        return True
                        
        return False