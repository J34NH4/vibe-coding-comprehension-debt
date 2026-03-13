from typing import Optional


class Solution:
    """Solution for finding the longest palindromic substring in a given string."""
    
    def longestPalindrome(self, s: str) -> str:
        """
        Find the longest palindromic substring in the given string.
        
        Args:
            s: The input string to search for palindromes
            
        Returns:
            The longest palindromic substring found in the input string
            
        Raises:
            ValueError: If input string is None
        """
        if s is None:
            raise ValueError("Input string cannot be None")
        
        if not s:
            return ""
        
        longest_palindrome_start: int = 0
        max_palindrome_length: int = 1
        
        for center_index in range(len(s)):
            # Check for odd-length palindromes centered at current index
            odd_length: int = self._expand_around_center(s, center_index, center_index)
            
            # Check for even-length palindromes centered between current and next index
            even_length: int = self._expand_around_center(s, center_index, center_index + 1)
            
            current_max_length: int = max(odd_length, even_length)
            
            if current_max_length > max_palindrome_length:
                max_palindrome_length = current_max_length
                # Calculate start position based on center and length
                longest_palindrome_start = center_index - (current_max_length - 1) // 2
        
        return s[longest_palindrome_start:longest_palindrome_start + max_palindrome_length]
    
    def _expand_around_center(self, s: str, left_index: int, right_index: int) -> int:
        """
        Expand around the center to find the length of palindrome.
        
        Args:
            s: The input string
            left_index: Left boundary index for expansion
            right_index: Right boundary index for expansion
            
        Returns:
            Length of the palindrome found by expanding around the center
        """
        while (left_index >= 0 and 
               right_index < len(s) and 
               s[left_index] == s[right_index]):
            left_index -= 1  # Expand left boundary
            right_index += 1  # Expand right boundary
        
        # Return length of palindrome (right_index - left_index - 1)
        return right_index - left_index - 1