from typing import Dict, Optional

class TrieNode:
    """A node in the Trie data structure."""
    
    def __init__(self) -> None:
        """Initialize a new TrieNode with empty children and end marker."""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False

class Trie:
    """A Trie (prefix tree) data structure for efficient string operations."""

    def __init__(self) -> None:
        """Initialize the trie with an empty root node."""
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie.
        
        Args:
            word: The word to insert into the trie.
            
        Raises:
            ValueError: If word is empty or None.
        """
        if not word:
            raise ValueError("Word cannot be empty or None")
            
        current_node: TrieNode = self.root
        
        for character in word:
            # Create new node if character doesn't exist
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        
        # Mark the end of the word
        current_node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Search for a complete word in the trie.
        
        Args:
            word: The word to search for.
            
        Returns:
            True if the word exists in the trie, False otherwise.
        """
        if not word:
            return False
            
        final_node: Optional[TrieNode] = self._find_node(word)
        return final_node is not None and final_node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """Check if any word in the trie starts with the given prefix.
        
        Args:
            prefix: The prefix to search for.
            
        Returns:
            True if any word starts with the prefix, False otherwise.
        """
        if not prefix:
            return True
            
        return self._find_node(prefix) is not None

    def _find_node(self, word: str) -> Optional[TrieNode]:
        """Helper method to find the node corresponding to a word/prefix.
        
        Args:
            word: The word or prefix to find.
            
        Returns:
            The TrieNode if found, None otherwise.
        """
        current_node: TrieNode = self.root
        
        for character in word:
            if character not in current_node.children:
                return None
            current_node = current_node.children[character]
        
        return current_node