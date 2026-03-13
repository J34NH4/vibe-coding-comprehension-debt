from typing import Set


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find the length of the longest substring without repeating characters.
        
        Args:
            s: Input string to analyze
            
        Returns:
            Length of longest substring without repeating characters
            
        Raises:
            TypeError: If input is not a string
        """
        if not isinstance(s, str):
            raise TypeError("Input must be a string")
            
        return self._sliding_window_approach(s)
    
    def _sliding_window_approach(self, input_string: str) -> int:
        """
        Use sliding window technique to find longest substring without repeats.
        
        Args:
            input_string: String to process
            
        Returns:
            Maximum length found
        """
        if not input_string:
            return 0
            
        character_set: Set[str] = set()
        left_pointer: int = 0
        max_length: int = 0
        
        for right_pointer in range(len(input_string)):
            current_character: str = input_string[right_pointer]
            
            # Shrink window until no duplicate exists
            while current_character in character_set:
                character_set.remove(input_string[left_pointer])
                left_pointer += 1
            
            # Add current character to set
            character_set.add(current_character)
            
            # Update maximum length if current window is larger
            current_window_size: int = right_pointer - left_pointer + 1
            max_length = max(max_length, current_window_size)
            
        return max_length