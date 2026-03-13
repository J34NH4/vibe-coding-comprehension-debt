from typing import Dict

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find the length of the longest substring without repeating characters.
        
        Uses sliding window technique with hash map to track character positions.
        
        Args:
            s: Input string to analyze
            
        Returns:
            Length of longest substring without repeating characters
        """
        if not s:
            return 0
            
        return self._find_longest_unique_substring(s)
    
    def _find_longest_unique_substring(self, input_string: str) -> int:
        """
        Helper method to find longest substring using sliding window approach.
        
        Args:
            input_string: String to process
            
        Returns:
            Maximum length of substring without repeating characters
        """
        character_position_map: Dict[str, int] = {}
        left_pointer: int = 0
        max_length: int = 0
        
        for right_pointer in range(len(input_string)):
            current_character: str = input_string[right_pointer]
            
            # If character seen before and within current window
            if current_character in character_position_map and character_position_map[current_character] >= left_pointer:
                left_pointer = character_position_map[current_character] + 1  # Move past duplicate
            
            character_position_map[current_character] = right_pointer  # Update character position
            current_window_length: int = right_pointer - left_pointer + 1
            max_length = max(max_length, current_window_length)  # Track maximum length
            
        return max_length