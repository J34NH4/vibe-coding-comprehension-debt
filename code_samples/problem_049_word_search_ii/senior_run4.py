from typing import List, Dict, Optional, Set

class TrieNode:
    """A node in the Trie data structure for efficient word prefix matching."""
    
    def __init__(self) -> None:
        """Initialize a new TrieNode with empty children and word flag."""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_word_end: bool = False
        self.word: Optional[str] = None

class Trie:
    """Trie data structure for efficient prefix-based word searching."""
    
    def __init__(self) -> None:
        """Initialize the Trie with an empty root node."""
        self.root: TrieNode = TrieNode()
    
    def insert_word(self, word: str) -> None:
        """Insert a word into the Trie structure.
        
        Args:
            word: The word to insert into the Trie
        """
        current_node: TrieNode = self.root
        
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        
        current_node.is_word_end = True
        current_node.word = word

class Solution:
    """Solution for finding all words from a dictionary that exist on a 2D board."""
    
    DIRECTIONS: List[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Find all words from the word list that can be constructed on the board.
        
        Args:
            board: 2D grid of characters
            words: List of words to search for on the board
            
        Returns:
            List of words found on the board
        """
        if not board or not board[0] or not words:
            return []
        
        # Build Trie from word list
        word_trie: Trie = self._build_trie(words)
        
        board_rows: int = len(board)
        board_cols: int = len(board[0])
        found_words: Set[str] = set()
        
        # Start DFS from each cell on the board
        for row_index in range(board_rows):
            for col_index in range(board_cols):
                visited_cells: Set[tuple[int, int]] = set()
                self._depth_first_search(
                    board, row_index, col_index, word_trie.root, 
                    visited_cells, found_words
                )
        
        return list(found_words)
    
    def _build_trie(self, words: List[str]) -> Trie:
        """Build a Trie from the given list of words.
        
        Args:
            words: List of words to insert into the Trie
            
        Returns:
            Constructed Trie containing all words
        """
        word_trie: Trie = Trie()
        
        for word in words:
            if word:  # Handle edge case of empty words
                word_trie.insert_word(word)
        
        return word_trie
    
    def _depth_first_search(
        self, 
        board: List[List[str]], 
        current_row: int, 
        current_col: int, 
        trie_node: TrieNode, 
        visited_cells: Set[tuple[int, int]], 
        found_words: Set[str]
    ) -> None:
        """Perform DFS to find words starting from current position.
        
        Args:
            board: 2D character grid
            current_row: Current row position
            current_col: Current column position
            trie_node: Current node in the Trie traversal
            visited_cells: Set of already visited cell coordinates
            found_words: Set to store found words
        """
        # Check boundary conditions
        if (current_row < 0 or current_row >= len(board) or 
            current_col < 0 or current_col >= len(board[0])):
            return
        
        # Check if cell already visited
        cell_position: tuple[int, int] = (current_row, current_col)
        if cell_position in visited_cells:
            return
        
        current_character: str = board[current_row][current_col]
        
        # Check if character exists in Trie
        if current_character not in trie_node.children:
            return
        
        next_trie_node: TrieNode = trie_node.children[current_character]
        
        # Mark current cell as visited
        visited_cells.add(cell_position)
        
        # Check if we found a complete word
        if next_trie_node.is_word_end and next_trie_node.word:
            found_words.add(next_trie_node.word)
        
        # Explore all four directions
        for row_delta, col_delta in self.DIRECTIONS:
            next_row: int = current_row + row_delta
            next_col: int = current_col + col_delta
            
            self._depth_first_search(
                board, next_row, next_col, next_trie_node, 
                visited_cells, found_words
            )
        
        # Backtrack: remove current cell from visited set
        visited_cells.remove(cell_position)