from typing import List, Set, Optional

class TrieNode:
    """Represents a node in the Trie data structure for efficient word searching."""
    
    def __init__(self) -> None:
        """Initialize a new TrieNode with empty children and word marker."""
        self.children: dict[str, 'TrieNode'] = {}
        self.word: Optional[str] = None

class Trie:
    """Trie data structure for storing and searching words efficiently."""
    
    def __init__(self) -> None:
        """Initialize the Trie with an empty root node."""
        self.root: TrieNode = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the Trie.
        
        Args:
            word: The word to insert into the Trie.
        """
        current_node = self.root
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        current_node.word = word  # Mark end of word

class Solution:
    """Solution for Word Search II problem using Trie and DFS."""
    
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Find all words from the word list that exist on the board.
        
        Args:
            board: 2D grid of characters to search in.
            words: List of words to find on the board.
            
        Returns:
            List of words found on the board.
            
        Raises:
            ValueError: If board is empty or words list is empty.
        """
        if not board or not board[0] or not words:
            return []
        
        # Build Trie from words list
        word_trie = self._build_trie(words)
        found_words: Set[str] = set()
        
        rows, cols = len(board), len(board[0])
        
        # Start DFS from each cell
        for row_index in range(rows):
            for col_index in range(cols):
                self._dfs_search(
                    board, row_index, col_index, word_trie.root, found_words
                )
        
        return list(found_words)
    
    def _build_trie(self, words: List[str]) -> Trie:
        """Build a Trie from the given list of words.
        
        Args:
            words: List of words to insert into the Trie.
            
        Returns:
            Constructed Trie containing all words.
        """
        word_trie = Trie()
        for word in words:
            word_trie.insert(word)
        return word_trie
    
    def _dfs_search(
        self, 
        board: List[List[str]], 
        row: int, 
        col: int, 
        trie_node: TrieNode, 
        found_words: Set[str]
    ) -> None:
        """Perform DFS search on the board to find words.
        
        Args:
            board: 2D grid of characters.
            row: Current row position.
            col: Current column position.
            trie_node: Current node in the Trie.
            found_words: Set to store found words.
        """
        # Check bounds
        if (row < 0 or row >= len(board) or 
            col < 0 or col >= len(board[0])):
            return
        
        current_character = board[row][col]
        
        # Check if character is already visited or not in Trie
        if (current_character == '#' or 
            current_character not in trie_node.children):
            return
        
        # Move to next Trie node
        next_trie_node = trie_node.children[current_character]
        
        # Check if we found a complete word
        if next_trie_node.word:
            found_words.add(next_trie_node.word)
            next_trie_node.word = None  # Avoid duplicates
        
        # Mark cell as visited
        board[row][col] = '#'
        
        # Explore all four directions
        for row_delta, col_delta in self.DIRECTIONS:
            new_row = row + row_delta
            new_col = col + col_delta
            self._dfs_search(board, new_row, new_col, next_trie_node, found_words)
        
        # Restore original character (backtrack)
        board[row][col] = current_character
        
        # Prune empty branches to optimize
        if not next_trie_node.children and not next_trie_node.word:
            del trie_node.children[current_character]