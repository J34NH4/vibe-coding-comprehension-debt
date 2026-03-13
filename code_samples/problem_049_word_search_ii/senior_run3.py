from typing import List, Set, Optional

class TrieNode:
    """Node in a Trie data structure for efficient word prefix matching."""
    
    def __init__(self) -> None:
        """Initialize a new TrieNode with empty children and no word marker."""
        self.children: dict[str, 'TrieNode'] = {}
        self.word: Optional[str] = None  # Store complete word at end nodes

class Trie:
    """Trie data structure for efficient word storage and prefix matching."""
    
    def __init__(self) -> None:
        """Initialize a new Trie with an empty root node."""
        self.root: TrieNode = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the Trie.
        
        Args:
            word: The word to insert into the Trie.
        """
        current_node: TrieNode = self.root
        
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        
        current_node.word = word  # Mark end of word

class Solution:
    """Solution for Word Search II problem using Trie and DFS."""
    
    # Direction vectors for exploring adjacent cells
    DIRECTIONS: List[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Find all words from the word list that exist on the board.
        
        Args:
            board: 2D grid of characters to search in.
            words: List of words to find on the board.
            
        Returns:
            List of words found on the board.
        """
        if not board or not board[0] or not words:
            return []
        
        # Build Trie from word list
        word_trie: Trie = self._build_trie(words)
        
        found_words: Set[str] = set()
        board_rows: int = len(board)
        board_cols: int = len(board[0])
        
        # Try starting DFS from each cell
        for row_index in range(board_rows):
            for col_index in range(board_cols):
                self._depth_first_search(
                    board, row_index, col_index, word_trie.root, found_words
                )
        
        return list(found_words)
    
    def _build_trie(self, words: List[str]) -> Trie:
        """Build a Trie from the given word list.
        
        Args:
            words: List of words to insert into the Trie.
            
        Returns:
            Constructed Trie containing all words.
        """
        word_trie: Trie = Trie()
        
        for word in words:
            if word:  # Skip empty words
                word_trie.insert(word)
        
        return word_trie
    
    def _depth_first_search(
        self,
        board: List[List[str]],
        row: int,
        col: int,
        trie_node: TrieNode,
        found_words: Set[str]
    ) -> None:
        """Perform DFS to find words starting from current position.
        
        Args:
            board: 2D character grid to search.
            row: Current row position.
            col: Current column position.
            trie_node: Current node in the Trie traversal.
            found_words: Set to store found words.
        """
        # Check bounds
        if not self._is_valid_position(board, row, col):
            return
        
        current_char: str = board[row][col]
        
        # Check if current character exists in Trie
        if current_char not in trie_node.children:
            return
        
        # Mark current cell as visited
        board[row][col] = '#'
        
        next_trie_node: TrieNode = trie_node.children[current_char]
        
        # Check if we found a complete word
        if next_trie_node.word is not None:
            found_words.add(next_trie_node.word)
            # Optimization: remove found word to avoid duplicates
            next_trie_node.word = None
        
        # Explore all four directions
        for delta_row, delta_col in self.DIRECTIONS:
            next_row: int = row + delta_row
            next_col: int = col + delta_col
            
            self._depth_first_search(
                board, next_row, next_col, next_trie_node, found_words
            )
        
        # Backtrack: restore original character
        board[row][col] = current_char
    
    def _is_valid_position(self, board: List[List[str]], row: int, col: int) -> bool:
        """Check if the given position is valid and unvisited.
        
        Args:
            board: 2D character grid.
            row: Row index to check.
            col: Column index to check.
            
        Returns:
            True if position is valid and unvisited, False otherwise.
        """
        return (
            0 <= row < len(board) and
            0 <= col < len(board[0]) and
            board[row][col] != '#'  # Not visited
        )