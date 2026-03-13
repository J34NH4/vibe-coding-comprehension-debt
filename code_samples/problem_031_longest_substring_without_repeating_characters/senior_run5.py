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
            TypeError: If input is not a string
        """
        if not isinstance(input_string, str):
            raise TypeError("Input must be a string")
            
        if not input_string:
            return 0
            
        return self._find_longest_unique_substring(input_string)
    
    def _find_longest_unique_substring(self, input_string: str) -> int:
        """
        Helper method to find longest unique substring using sliding window.
        
        Args:
            input_string: The input string to analyze
            
        Returns:
            The length of the longest unique substring
        """
        character_to_index_map: Dict[str, int] = {}
        left_pointer: int = 0
        maximum_length: int = 0
        
        for right_pointer in range(len(input_string)):
            current_character: str = input_string[right_pointer]
            
            # If character is already seen and within current window
            if current_character in character_to_index_map and character_to_index_map[current_character] >= left_pointer:
                left_pointer = character_to_index_map[current_character] + 1  # Move left pointer past duplicate
            
            character_to_index_map[current_character] = right_pointer  # Update character position
            current_window_length: int = right_pointer - left_pointer + 1
            maximum_length = max(maximum_length, current_window_length)  # Update max length if needed
            
        return maximum_length