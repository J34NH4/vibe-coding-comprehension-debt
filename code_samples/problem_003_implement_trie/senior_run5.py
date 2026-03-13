from typing import Optional, Dict

class TrieNode:
    """A node in the Trie data structure."""
    
    def __init__(self) -> None:
        """Initialize a TrieNode with empty children and end marker."""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False

class Trie:
    """
    A Trie (prefix tree) data structure for efficient string operations.
    
    Supports insertion, search, and prefix matching operations.
    """

    def __init__(self) -> None:
        """Initialize your data structure here."""
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        
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
        
        # Mark end of word
        current_node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        
        Args:
            word: The word to search for.
            
        Returns:
            True if word exists in trie, False otherwise.
        """
        if not word:
            return False
            
        final_node: Optional[TrieNode] = self._find_node(word)
        return final_node is not None and final_node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        
        Args:
            prefix: The prefix to search for.
            
        Returns:
            True if any word starts with prefix, False otherwise.
        """
        if not prefix:
            return True  # Empty prefix matches everything
            
        return self._find_node(prefix) is not None

    def _find_node(self, word_or_prefix: str) -> Optional[TrieNode]:
        """
        Helper method to find the node corresponding to a word or prefix.
        
        Args:
            word_or_prefix: The string to traverse in the trie.
            
        Returns:
            The TrieNode at the end of traversal, or None if path doesn't exist.
        """
        current_node: TrieNode = self.root
        
        for character in word_or_prefix:
            if character not in current_node.children:
                return None  # Path doesn't exist
            current_node = current_node.children[character]
            
        return current_node