from typing import List, Set


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        Determines if a string can be segmented into words from a dictionary.
        
        Args:
            s: The input string to segment
            wordDict: List of valid dictionary words
            
        Returns:
            True if string can be segmented, False otherwise
            
        Raises:
            ValueError: If input string is None
        """
        if s is None:
            raise ValueError("Input string cannot be None")
            
        if not s:
            return True
            
        if not wordDict:
            return False
            
        return self._can_break_with_memoization(s, wordDict)
    
    def _can_break_with_memoization(self, target_string: str, word_dictionary: List[str]) -> bool:
        """
        Uses dynamic programming with memoization to check if string can be broken.
        
        Args:
            target_string: String to segment
            word_dictionary: Available words for segmentation
            
        Returns:
            True if segmentation is possible, False otherwise
        """
        string_length = len(target_string)
        word_set = set(word_dictionary)  # O(1) lookup time
        memo_cache = {}
        
        return self._helper_can_break(target_string, 0, word_set, memo_cache)
    
    def _helper_can_break(self, target_string: str, start_index: int, 
                         word_set: Set[str], memo_cache: dict) -> bool:
        """
        Recursive helper function with memoization for word break problem.
        
        Args:
            target_string: The string to segment
            start_index: Current starting position in the string
            word_set: Set of valid words for O(1) lookup
            memo_cache: Memoization cache to avoid recomputation
            
        Returns:
            True if substring from start_index can be segmented, False otherwise
        """
        if start_index == len(target_string):
            return True
            
        if start_index in memo_cache:
            return memo_cache[start_index]
        
        # Try all possible word endings from current position
        for end_index in range(start_index + 1, len(target_string) + 1):
            current_word = target_string[start_index:end_index]
            
            # If current word exists in dictionary and remaining string can be broken
            if (current_word in word_set and 
                self._helper_can_break(target_string, end_index, word_set, memo_cache)):
                memo_cache[start_index] = True
                return True
        
        memo_cache[start_index] = False
        return False