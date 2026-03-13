from collections import defaultdict, Counter
from typing import Dict, Tuple, Optional

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Find the minimum window substring of s that contains all characters in t.
        
        Args:
            s: Source string to search in
            t: Target string containing required characters
            
        Returns:
            Minimum window substring, or empty string if no valid window exists
        """
        if not s or not t or len(s) < len(t):
            return ""
        
        # Count characters in target string
        target_char_count = Counter(t)
        required_unique_chars = len(target_char_count)
        
        # Initialize sliding window variables
        left_pointer = 0
        right_pointer = 0
        current_window_count = defaultdict(int)
        formed_chars_count = 0  # Number of unique chars in current window with desired frequency
        
        # Result tracking
        min_window_length = float('inf')
        min_window_start = 0
        min_window_end = 0
        
        while right_pointer < len(s):
            # Expand window by including character at right pointer
            right_char = s[right_pointer]
            current_window_count[right_char] += 1
            
            # Check if current character frequency matches target frequency
            if right_char in target_char_count and current_window_count[right_char] == target_char_count[right_char]:
                formed_chars_count += 1
            
            # Contract window from left until it ceases to be desirable
            while left_pointer <= right_pointer and formed_chars_count == required_unique_chars:
                current_window_length = right_pointer - left_pointer + 1
                
                # Update minimum window if current is smaller
                if current_window_length < min_window_length:
                    min_window_length = current_window_length
                    min_window_start = left_pointer
                    min_window_end = right_pointer
                
                # Contract window from left
                left_char = s[left_pointer]
                current_window_count[left_char] -= 1
                
                # Check if removing left character breaks the condition
                if left_char in target_char_count and current_window_count[left_char] < target_char_count[left_char]:
                    formed_chars_count -= 1
                
                left_pointer += 1
            
            right_pointer += 1
        
        # Return minimum window or empty string if no valid window found
        return "" if min_window_length == float('inf') else s[min_window_start:min_window_end + 1]