from collections import defaultdict, Counter
from typing import Optional

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Find the minimum window substring of s that contains all characters of t.
        
        Args:
            s: The source string to search in
            t: The target string containing required characters
            
        Returns:
            The minimum window substring, or empty string if no valid window exists
        """
        if not s or not t or len(s) < len(t):
            return ""
            
        # Count characters needed from target string
        target_char_count = Counter(t)
        required_unique_chars = len(target_char_count)
        
        # Sliding window variables
        left_pointer = 0
        right_pointer = 0
        
        # Track characters in current window
        window_char_count = defaultdict(int)
        formed_unique_chars = 0  # Number of unique chars in window with desired frequency
        
        # Result tracking
        min_window_length = float('inf')
        min_window_left = 0
        min_window_right = 0
        
        while right_pointer < len(s):
            # Expand window by including character at right pointer
            current_char = s[right_pointer]
            window_char_count[current_char] += 1
            
            # Check if current character frequency matches target frequency
            if current_char in target_char_count and window_char_count[current_char] == target_char_count[current_char]:
                formed_unique_chars += 1
            
            # Contract window if all required characters are present
            while left_pointer <= right_pointer and formed_unique_chars == required_unique_chars:
                current_window_length = right_pointer - left_pointer + 1
                
                # Update minimum window if current is smaller
                if current_window_length < min_window_length:
                    min_window_length = current_window_length
                    min_window_left = left_pointer
                    min_window_right = right_pointer
                
                # Remove leftmost character from window
                left_char = s[left_pointer]
                window_char_count[left_char] -= 1
                
                # Update formed count if removing character breaks requirement
                if left_char in target_char_count and window_char_count[left_char] < target_char_count[left_char]:
                    formed_unique_chars -= 1
                
                left_pointer += 1
            
            right_pointer += 1
        
        # Return minimum window or empty string if no valid window found
        return "" if min_window_length == float('inf') else s[min_window_left:min_window_right + 1]