from typing import List, Set


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        Determines if string can be segmented into dictionary words.
        
        Args:
            s: The input string to segment
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
            
        if not wordDict:
            return False
            
        word_set = self._convert_to_word_set(wordDict)
        memo_cache = {}
        
        return self._can_break_with_memo(s, word_set, memo_cache, start_index=0)
    
    def _convert_to_word_set(self, word_list: List[str]) -> Set[str]:
        """
        Converts word list to set for O(1) lookup time.
        
        Args:
            word_list: List of dictionary words
            
        Returns:
            Set containing all dictionary words
        """
        return set(word_list)
    
    def _can_break_with_memo(self, target_string: str, word_set: Set[str], 
                            memo_cache: dict, start_index: int) -> bool:
        """
        Recursively checks if substring can be broken using memoization.
        
        Args:
            target_string: The original string being processed
            word_set: Set of valid dictionary words
            memo_cache: Cache to store previously computed results
            start_index: Starting position in the string
            
        Returns:
            True if substring from start_index can be segmented
        """
        # Base case: reached end of string
        if start_index == len(target_string):
            return True
            
        # Check memoization cache
        if start_index in memo_cache:
            return memo_cache[start_index]
        
        # Try all possible word endings from current position
        for end_index in range(start_index + 1, len(target_string) + 1):
            current_word = target_string[start_index:end_index]
            
            # If current word exists in dictionary
            if current_word in word_set:
                # Recursively check remaining substring
                if self._can_break_with_memo(target_string, word_set, memo_cache, end_index):
                    memo_cache[start_index] = True
                    return True
        
        # No valid segmentation found from this position
        memo_cache[start_index] = False
        return False