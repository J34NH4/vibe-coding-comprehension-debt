from typing import Dict

class Solution:
    def lengthOfLongestSubstring(self, input_string: str) -> int:
        """
        Find the length of the longest substring without repeating characters.
        
        Args:
            input_string: The input string to analyze
            
        Returns:
            The length of the longest substring without repeating characters
            
        Raises:
            ValueError: If input_string is None
        """
        if input_string is None:
            raise ValueError("Input string cannot be None")
            
        return self._find_longest_unique_substring(input_string)
    
    def _find_longest_unique_substring(self, input_string: str) -> int:
        """
        Helper method to find longest substring using sliding window approach.
        
        Args:
            input_string: The string to process
            
        Returns:
            Length of longest substring without repeating characters
        """
        if not input_string:
            return 0
            
        character_positions: Dict[str, int] = {}  # Maps character to its latest position
        left_pointer: int = 0  # Left boundary of current window
        max_length: int = 0  # Maximum length found so far
        
        for right_pointer in range(len(input_string)):
            current_character: str = input_string[right_pointer]
            
            # If character is already in current window, move left pointer
            if current_character in character_positions and character_positions[current_character] >= left_pointer:
                left_pointer = character_positions[current_character] + 1
            
            # Update character's latest position
            character_positions[current_character] = right_pointer
            
            # Calculate current window length and update maximum
            current_length: int = right_pointer - left_pointer + 1
            max_length = max(max_length, current_length)
            
        return max_length