from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        Determine if a word exists in the board using DFS with backtracking.
        
        Args:
            board: 2D grid of characters
            word: Target word to search for
            
        Returns:
            True if word exists in the board, False otherwise
        """
        if not board or not board[0] or not word:
            return False
            
        rows = len(board)
        columns = len(board[0])
        
        def _backtrack_search(row: int, col: int, word_index: int) -> bool:
            """
            Recursively search for word using DFS with backtracking.
            
            Args:
                row: Current row position
                col: Current column position  
                word_index: Current index in the target word
                
            Returns:
                True if remaining word can be found from current position
            """
            # Base case: found complete word
            if word_index == len(word):
                return True
                
            # Check bounds and character match
            if (row < 0 or row >= rows or 
                col < 0 or col >= columns or 
                board[row][col] != word[word_index]):
                return False
                
            # Mark current cell as visited
            original_character = board[row][col]
            board[row][col] = '#'
            
            # Explore all four directions
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            found = False
            
            for row_offset, col_offset in directions:
                next_row = row + row_offset
                next_col = col + col_offset
                
                if _backtrack_search(next_row, next_col, word_index + 1):
                    found = True
                    break
                    
            # Backtrack: restore original character
            board[row][col] = original_character
            
            return found
        
        # Try starting from each cell in the board
        for start_row in range(rows):
            for start_col in range(columns):
                if _backtrack_search(start_row, start_col, 0):
                    return True
                    
        return False