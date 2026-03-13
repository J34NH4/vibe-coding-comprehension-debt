from typing import Dict, Set

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find the length of the longest substring without repeating characters.
        
        Args:
            s: Input string to analyze
            
        Returns:
            Length of the longest substring without repeating characters
            
        Raises:
            ValueError: If input string is None
        """
        if s is None:
            raise ValueError("Input string cannot be None")
        
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
        
        character_positions: Dict[str, int] = {}  # Track last seen position of each character
        maximum_length: int = 0
        window_start: int = 0
        
        for current_position, current_character in enumerate(input_string):
            # If character was seen and is within current window
            if (current_character in character_positions and 
                character_positions[current_character] >= window_start):
                # Move window start to position after the duplicate
                window_start = character_positions[current_character] + 1
            
            # Update character's last seen position
            character_positions[current_character] = current_position
            
            # Calculate current window length and update maximum
            current_window_length = current_position - window_start + 1
            maximum_length = max(maximum_length, current_window_length)
        
        return maximum_length