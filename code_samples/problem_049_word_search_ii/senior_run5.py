from typing import List, Set, Tuple

class TrieNode:
    """A node in the trie data structure for efficient word searching."""
    
    def __init__(self) -> None:
        """Initialize a new TrieNode."""
        self.children = {}
        self.is_word = False
        self.word = ""

class Trie:
    """Trie data structure for efficient prefix-based word searching."""
    
    def __init__(self) -> None:
        """Initialize a new Trie."""
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the trie.
        
        Args:
            word: The word to insert into the trie.
        """
        current_node = self.root
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        current_node.is_word = True
        current_node.word = word

class Solution:
    """Solution for finding all words from a dictionary that exist on a 2D board."""
    
    def __init__(self) -> None:
        """Initialize the solution."""
        self.DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Find all words from the word list that can be constructed on the board.
        
        Args:
            board: 2D grid of characters.
            words: List of words to search for on the board.
            
        Returns:
            List of words found on the board.
        """
        if not board or not board[0] or not words:
            return []
        
        # Build trie from word list
        word_trie = self._build_trie(words)
        found_words = set()
        
        # Search for words starting from each cell
        for row_index in range(len(board)):
            for column_index in range(len(board[0])):
                visited_positions = set()
                self._depth_first_search(
                    board, row_index, column_index, word_trie.root, 
                    visited_positions, found_words
                )
        
        return list(found_words)
    
    def _build_trie(self, words: List[str]) -> Trie:
        """Build a trie from the given list of words.
        
        Args:
            words: List of words to insert into the trie.
            
        Returns:
            Constructed Trie containing all words.
        """
        word_trie = Trie()
        for word in words:
            word_trie.insert(word)
        return word_trie
    
    def _depth_first_search(
        self, 
        board: List[List[str]], 
        row: int, 
        column: int, 
        trie_node: TrieNode, 
        visited_positions: Set[Tuple[int, int]], 
        found_words: Set[str]
    ) -> None:
        """Perform DFS to find words on the board using the trie.
        
        Args:
            board: 2D grid of characters.
            row: Current row position.
            column: Current column position.
            trie_node: Current node in the trie.
            visited_positions: Set of already visited positions in current path.
            found_words: Set to store found words.
        """
        # Check bounds and if position already visited
        if (row < 0 or row >= len(board) or 
            column < 0 or column >= len(board[0]) or 
            (row, column) in visited_positions):
            return
        
        current_character = board[row][column]
        
        # Check if current character exists in trie
        if current_character not in trie_node.children:
            return
        
        next_trie_node = trie_node.children[current_character]
        
        # If we found a complete word, add it to results
        if next_trie_node.is_word:
            found_words.add(next_trie_node.word)
        
        # Mark current position as visited
        visited_positions.add((row, column))
        
        # Explore all four directions
        for row_delta, column_delta in self.DIRECTIONS:
            new_row = row + row_delta
            new_column = column + column_delta
            self._depth_first_search(
                board, new_row, new_column, next_trie_node, 
                visited_positions, found_words
            )
        
        # Backtrack: remove current position from visited
        visited_positions.remove((row, column))