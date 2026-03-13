from typing import List, Set, Optional

class TrieNode:
    """Node structure for Trie data structure."""
    
    def __init__(self) -> None:
        """Initialize a new TrieNode."""
        self.children: dict = {}
        self.word: Optional[str] = None

class Solution:
    """Solution class for Word Search II problem using Trie optimization."""
    
    def __init__(self) -> None:
        """Initialize solution with direction vectors."""
        self.DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Find all words from the word list that can be constructed from letters 
        of sequentially adjacent cells on the board.
        
        Args:
            board: 2D grid of characters
            words: List of words to search for
            
        Returns:
            List of words found on the board
        """
        if not board or not board[0] or not words:
            return []
            
        # Build trie from words list
        root_node = self._build_trie(words)
        
        found_words: Set[str] = set()
        rows, cols = len(board), len(board[0])
        
        # Start DFS from each cell
        for row in range(rows):
            for col in range(cols):
                self._dfs_search(board, row, col, root_node, found_words)
        
        return list(found_words)
    
    def _build_trie(self, words: List[str]) -> TrieNode:
        """
        Build a trie data structure from the given words list.
        
        Args:
            words: List of words to insert into trie
            
        Returns:
            Root node of the constructed trie
        """
        root_node = TrieNode()
        
        for word in words:
            current_node = root_node
            for character in word:
                if character not in current_node.children:
                    current_node.children[character] = TrieNode()
                current_node = current_node.children[character]
            current_node.word = word  # Mark end of word
            
        return root_node
    
    def _dfs_search(self, board: List[List[str]], row: int, col: int, 
                   trie_node: TrieNode, found_words: Set[str]) -> None:
        """
        Perform depth-first search to find words starting from given position.
        
        Args:
            board: 2D grid of characters
            row: Current row position
            col: Current column position
            trie_node: Current node in trie traversal
            found_words: Set to store found words
        """
        # Boundary and validity checks
        if (row < 0 or row >= len(board) or 
            col < 0 or col >= len(board[0])):
            return
            
        current_char = board[row][col]
        
        # Check if character already visited or not in trie
        if current_char == '#' or current_char not in trie_node.children:
            return
            
        # Move to next trie node
        next_trie_node = trie_node.children[current_char]
        
        # Check if we found a complete word
        if next_trie_node.word:
            found_words.add(next_trie_node.word)
            next_trie_node.word = None  # Avoid duplicate additions
        
        # Mark current cell as visited
        board[row][col] = '#'
        
        # Explore all four directions
        for delta_row, delta_col in self.DIRECTIONS:
            new_row = row + delta_row
            new_col = col + delta_col
            self._dfs_search(board, new_row, new_col, next_trie_node, found_words)
        
        # Restore original character (backtrack)
        board[row][col] = current_char
        
        # Optimization: remove leaf nodes to reduce search space
        if not next_trie_node.children:
            del trie_node.children[current_char]