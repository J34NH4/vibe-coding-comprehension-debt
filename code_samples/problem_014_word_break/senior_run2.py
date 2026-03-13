from typing import List, Set


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        Determines if string can be segmented into dictionary words.
        
        Args:
            s: Input string to segment
            wordDict: List of valid dictionary words
            
        Returns:
            True if string can be segmented, False otherwise
            
        Raises:
            ValueError: If input string is None or wordDict is None
        """
        if s is None or wordDict is None:
            raise ValueError("Input string and word dictionary cannot be None")
            
        if not s:
            return True
            
        word_set = self._convert_to_word_set(wordDict)
        memo_cache = {}
        
        return self._can_break_string(s, word_set, 0, memo_cache)
    
    def _convert_to_word_set(self, word_list: List[str]) -> Set[str]:
        """
        Converts word list to set for O(1) lookup time.
        
        Args:
            word_list: List of dictionary words
            
        Returns:
            Set containing all dictionary words
        """
        return set(word_list)
    
    def _can_break_string(self, target_string: str, word_set: Set[str], 
                         start_index: int, memo_cache: dict) -> bool:
        """
        Recursively checks if string can be broken from start_index.
        
        Args:
            target_string: String to segment
            word_set: Set of valid words
            start_index: Current position in string
            memo_cache: Memoization cache for optimization
            
        Returns:
            True if string can be segmented from start_index
        """
        # Base case: reached end of string
        if start_index == len(target_string):
            return True
            
        # Check memoization cache
        if start_index in memo_cache:
            return memo_cache[start_index]
        
        # Try all possible word endings from current position
        for end_index in range(start_index + 1, len(target_string) + 1):
            current_substring = target_string[start_index:end_index]
            
            # If current substring is valid word and rest can be segmented
            if (current_substring in word_set and 
                self._can_break_string(target_string, word_set, end_index, memo_cache)):
                memo_cache[start_index] = True
                return True
        
        # No valid segmentation found from this position
        memo_cache[start_index] = False
        return False