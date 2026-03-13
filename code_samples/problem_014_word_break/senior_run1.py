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
            ValueError: If input string is None
        """
        if s is None:
            raise ValueError("Input string cannot be None")
            
        if not s:
            return True
            
        word_set = self._convert_to_word_set(wordDict)
        return self._can_segment_string(s, word_set)
    
    def _convert_to_word_set(self, word_dict: List[str]) -> Set[str]:
        """
        Converts word dictionary list to set for O(1) lookup.
        
        Args:
            word_dict: List of dictionary words
            
        Returns:
            Set containing all dictionary words
        """
        return set(word_dict) if word_dict else set()
    
    def _can_segment_string(self, target_string: str, word_set: Set[str]) -> bool:
        """
        Uses dynamic programming to check if string can be segmented.
        
        Args:
            target_string: String to segment
            word_set: Set of valid words for segmentation
            
        Returns:
            True if segmentation is possible, False otherwise
        """
        string_length = len(target_string)
        # dp[i] represents if substring s[0:i] can be segmented
        dp_table = [False] * (string_length + 1)
        dp_table[0] = True  # Empty string can always be segmented
        
        for current_position in range(1, string_length + 1):
            for word_start_position in range(current_position):
                # Check if prefix can be segmented and current word exists
                if (dp_table[word_start_position] and 
                    self._is_valid_word_at_position(target_string, word_start_position, 
                                                  current_position, word_set)):
                    dp_table[current_position] = True
                    break  # Found valid segmentation for this position
                    
        return dp_table[string_length]
    
    def _is_valid_word_at_position(self, target_string: str, start_index: int, 
                                 end_index: int, word_set: Set[str]) -> bool:
        """
        Checks if substring at given position exists in word set.
        
        Args:
            target_string: Original string
            start_index: Starting position of substring
            end_index: Ending position of substring (exclusive)
            word_set: Set of valid dictionary words
            
        Returns:
            True if substring is a valid word, False otherwise
        """
        current_word = target_string[start_index:end_index]
        return current_word in word_set