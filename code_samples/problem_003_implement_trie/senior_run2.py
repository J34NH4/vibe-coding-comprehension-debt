class TrieNode:
    """A node in the Trie data structure."""
    
    def __init__(self) -> None:
        """Initialize a new TrieNode with empty children and end marker."""
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False


class Trie:
    """
    A Trie (prefix tree) data structure implementation.
    
    Supports insertion, search, and prefix matching operations.
    """

    def __init__(self) -> None:
        """Initialize the Trie with an empty root node."""
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.
        
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
        """
        Search for a complete word in the trie.
        
        Args:
            word: The word to search for.
            
        Returns:
            True if the word exists in the trie, False otherwise.
        """
        if not word:
            return False
            
        target_node: TrieNode | None = self._find_node(word)
        return target_node is not None and target_node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
        Check if any word in the trie starts with the given prefix.
        
        Args:
            prefix: The prefix to search for.
            
        Returns:
            True if any word starts with the prefix, False otherwise.
        """
        if not prefix:
            return True
            
        return self._find_node(prefix) is not None

    def _find_node(self, word_or_prefix: str) -> TrieNode | None:
        """
        Find the node corresponding to the given word or prefix.
        
        Args:
            word_or_prefix: The string to find in the trie.
            
        Returns:
            The TrieNode if found, None otherwise.
        """
        current_node: TrieNode = self.root
        
        for character in word_or_prefix:
            if character not in current_node.children:
                return None  # Path doesn't exist
            current_node = current_node.children[character]
        
        return current_node