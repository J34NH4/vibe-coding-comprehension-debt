from collections import defaultdict
from typing import Dict, Tuple

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Find the minimum window substring of s that contains all characters in t.
        
        Args:
            s: Source string to search within
            t: Target string containing required characters
            
        Returns:
            Minimum window substring, or empty string if no valid window exists
        """
        if not s or not t or len(s) < len(t):
            return ""
        
        # Build frequency map for target string
        target_char_count = self._build_character_frequency_map(t)
        required_unique_chars = len(target_char_count)
        
        # Sliding window variables
        left_pointer = 0
        right_pointer = 0
        formed_chars_count = 0
        
        # Track characters in current window
        window_char_count: Dict[str, int] = defaultdict(int)
        
        # Track minimum window
        min_window_length = float('inf')
        min_window_left = 0
        min_window_right = 0
        
        while right_pointer < len(s):
            # Expand window by including character at right pointer
            current_char = s[right_pointer]
            window_char_count[current_char] += 1
            
            # Check if current character frequency matches target frequency
            if (current_char in target_char_count and 
                window_char_count[current_char] == target_char_count[current_char]):
                formed_chars_count += 1
            
            # Contract window from left while it remains valid
            while left_pointer <= right_pointer and formed_chars_count == required_unique_chars:
                current_window_length = right_pointer - left_pointer + 1
                
                # Update minimum window if current is smaller
                if current_window_length < min_window_length:
                    min_window_length = current_window_length
                    min_window_left = left_pointer
                    min_window_right = right_pointer
                
                # Remove leftmost character from window
                left_char = s[left_pointer]
                window_char_count[left_char] -= 1
                
                if (left_char in target_char_count and 
                    window_char_count[left_char] < target_char_count[left_char]):
                    formed_chars_count -= 1
                
                left_pointer += 1
            
            right_pointer += 1
        
        return "" if min_window_length == float('inf') else s[min_window_left:min_window_right + 1]
    
    def _build_character_frequency_map(self, target_string: str) -> Dict[str, int]:
        """
        Build frequency map for characters in target string.
        
        Args:
            target_string: String to analyze character frequencies
            
        Returns:
            Dictionary mapping characters to their frequencies
        """
        char_frequency_map: Dict[str, int] = defaultdict(int)
        
        for character in target_string:
            char_frequency_map[character] += 1
        
        return char_frequency_map