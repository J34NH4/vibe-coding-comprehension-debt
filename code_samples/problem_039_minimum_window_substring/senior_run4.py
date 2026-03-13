from collections import Counter, defaultdict
from typing import Optional

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Find the minimum window substring of s that contains all characters in t.
        
        Args:
            s: The source string to search in
            t: The target string containing characters to find
            
        Returns:
            The minimum window substring, or empty string if no valid window exists
        """
        if not s or not t or len(s) < len(t):
            return ""
        
        # Count characters needed from target string
        target_char_count = Counter(t)
        required_unique_chars = len(target_char_count)
        
        # Initialize sliding window variables
        left_pointer = 0
        right_pointer = 0
        formed_unique_chars = 0  # Number of unique chars in current window with desired frequency
        
        # Track character frequencies in current window
        window_char_count = defaultdict(int)
        
        # Track minimum window found
        minimum_window_length = float('inf')
        minimum_window_start = 0
        minimum_window_end = 0
        
        while right_pointer < len(s):
            # Expand window by including character at right pointer
            current_char = s[right_pointer]
            window_char_count[current_char] += 1
            
            # Check if current character's frequency matches required frequency
            if current_char in target_char_count and window_char_count[current_char] == target_char_count[current_char]:
                formed_unique_chars += 1
            
            # Contract window from left while it's valid
            while left_pointer <= right_pointer and formed_unique_chars == required_unique_chars:
                current_window_length = right_pointer - left_pointer + 1
                
                # Update minimum window if current is smaller
                if current_window_length < minimum_window_length:
                    minimum_window_length = current_window_length
                    minimum_window_start = left_pointer
                    minimum_window_end = right_pointer
                
                # Remove leftmost character from window
                left_char = s[left_pointer]
                window_char_count[left_char] -= 1
                
                # Check if removing left character breaks validity
                if left_char in target_char_count and window_char_count[left_char] < target_char_count[left_char]:
                    formed_unique_chars -= 1
                
                left_pointer += 1
            
            right_pointer += 1
        
        # Return minimum window or empty string if none found
        return "" if minimum_window_length == float('inf') else s[minimum_window_start:minimum_window_end + 1]