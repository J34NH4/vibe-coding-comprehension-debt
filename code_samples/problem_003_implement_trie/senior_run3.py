class TrieNode:
    """Represents a single node in the Trie data structure."""
    
    def __init__(self):
        """Initialize a new TrieNode with empty children and end marker."""
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False


class Trie:
    """
    A Trie (prefix tree) data structure for efficient string operations.
    
    Supports insertion, search, and prefix matching operations.
    """

    def __init__(self):
        """Initialize the Trie with an empty root node."""
        self.root_node: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.
        
        Args:
            word: The word to insert into the trie.
            
        Raises:
            TypeError: If word is not a string.
        """
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
            
        current_node: TrieNode = self.root_node
        
        # Traverse through each character in the word
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()  # Create new node if path doesn't exist
            current_node = current_node.children[character]
        
        current_node.is_end_of_word = True  # Mark the end of the inserted word

    def search(self, word: str) -> bool:
        """
        Search for a complete word in the trie.
        
        Args:
            word: The word to search for.
            
        Returns:
            True if the word exists in the trie, False otherwise.
            
        Raises:
            TypeError: If word is not a string.
        """
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
            
        final_node: TrieNode | None = self._find_node_for_prefix(word)
        return final_node is not None and final_node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
        Check if any word in the trie starts with the given prefix.
        
        Args:
            prefix: The prefix to search for.
            
        Returns:
            True if any word starts with the prefix, False otherwise.
            
        Raises:
            TypeError: If prefix is not a string.
        """
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")
            
        return self._find_node_for_prefix(prefix) is not None

    def _find_node_for_prefix(self, prefix: str) -> TrieNode | None:
        """
        Helper method to find the node corresponding to a given prefix.
        
        Args:
            prefix: The prefix to find the node for.
            
        Returns:
            The TrieNode at the end of the prefix path, or None if prefix doesn't exist.
        """
        current_node: TrieNode = self.root_node
        
        # Traverse through each character in the prefix
        for character in prefix:
            if character not in current_node.children:
                return None  # Prefix doesn't exist in trie
            current_node = current_node.children[character]
        
        return current_node