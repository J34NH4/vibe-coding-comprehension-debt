from typing import List, Set


class Solution:
    """Solution for the Word Break problem using dynamic programming."""
    
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        Determines if a string can be segmented into dictionary words.
        
        Args:
            s: The input string to segment
            wordDict: List of valid dictionary words
            
        Returns:
            True if string can be segmented, False otherwise
            
        Raises:
            TypeError: If inputs are not of expected types
        """
        if not isinstance(s, str) or not isinstance(wordDict, list):
            raise TypeError("Invalid input types")
            
        if not s:
            return True
            
        if not wordDict:
            return False
            
        word_set = self._convert_to_word_set(wordDict)
        string_length = len(s)
        
        # dp[i] represents if s[0:i] can be segmented
        dynamic_programming_table = self._initialize_dp_table(string_length)
        
        return self._fill_dp_table(s, word_set, dynamic_programming_table, string_length)
    
    def _convert_to_word_set(self, word_dict: List[str]) -> Set[str]:
        """
        Converts word dictionary list to set for O(1) lookup.
        
        Args:
            word_dict: List of dictionary words
            
        Returns:
            Set containing all dictionary words
        """
        return set(word_dict)
    
    def _initialize_dp_table(self, string_length: int) -> List[bool]:
        """
        Initializes the dynamic programming table.
        
        Args:
            string_length: Length of the input string
            
        Returns:
            Boolean list initialized with base case
        """
        dp_table = [False] * (string_length + 1)
        dp_table[0] = True  # Empty string can always be segmented
        return dp_table
    
    def _fill_dp_table(self, input_string: str, word_set: Set[str], 
                      dp_table: List[bool], string_length: int) -> bool:
        """
        Fills the dynamic programming table using bottom-up approach.
        
        Args:
            input_string: The string to segment
            word_set: Set of valid dictionary words
            dp_table: The DP table to fill
            string_length: Length of input string
            
        Returns:
            True if entire string can be segmented
        """
        for current_position in range(1, string_length + 1):
            if self._can_segment_at_position(input_string, word_set, dp_table, current_position):
                dp_table[current_position] = True
                
        return dp_table[string_length]
    
    def _can_segment_at_position(self, input_string: str, word_set: Set[str], 
                                dp_table: List[bool], current_position: int) -> bool:
        """
        Checks if string can be segmented up to current position.
        
        Args:
            input_string: The string being processed
            word_set: Set of valid dictionary words
            dp_table: Current state of DP table
            current_position: Position to check segmentation for
            
        Returns:
            True if segmentation is possible at current position
        """
        for previous_position in range(current_position):
            if dp_table[previous_position]:  # Previous segment is valid
                current_substring = input_string[previous_position:current_position]
                if current_substring in word_set:  # Current word is in dictionary
                    return True
                    
        return False