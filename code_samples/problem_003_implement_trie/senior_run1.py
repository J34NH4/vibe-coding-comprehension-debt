from typing import Optional, Dict

class TrieNode:
    """A node in the Trie data structure.
    
    Each node contains a dictionary of children nodes and a flag
    indicating if this node represents the end of a word.
    """
    
    def __init__(self) -> None:
        """Initialize a new TrieNode."""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False

class Trie:
    """A Trie (prefix tree) data structure implementation.
    
    Supports insertion of words, searching for complete words,
    and checking if any words start with a given prefix.
    """

    def __init__(self) -> None:
        """Initialize your data structure here."""
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the trie.
        
        Args:
            word: The word to insert into the trie.
        """
        if not word:
            return
            
        current_node: TrieNode = self.root
        
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        
        current_node.is_end_of_word = True  # Mark end of word

    def search(self, word: str) -> bool:
        """Returns if the word is in the trie.
        
        Args:
            word: The word to search for in the trie.
            
        Returns:
            True if the word exists in the trie, False otherwise.
        """
        if not word:
            return False
            
        final_node: Optional[TrieNode] = self._find_node(word)
        return final_node is not None and final_node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """Returns if there is any word in the trie that starts with the given prefix.
        
        Args:
            prefix: The prefix to search for in the trie.
            
        Returns:
            True if any word in the trie starts with the prefix, False otherwise.
        """
        if not prefix:
            return True
            
        return self._find_node(prefix) is not None

    def _find_node(self, word_or_prefix: str) -> Optional[TrieNode]:
        """Helper method to find the node corresponding to a word or prefix.
        
        Args:
            word_or_prefix: The string to search for in the trie.
            
        Returns:
            The TrieNode if found, None otherwise.
        """
        current_node: TrieNode = self.root
        
        for character in word_or_prefix:
            if character not in current_node.children:
                return None
            current_node = current_node.children[character]
        
        return current_node