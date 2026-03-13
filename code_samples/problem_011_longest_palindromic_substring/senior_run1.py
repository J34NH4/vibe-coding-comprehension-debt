from typing import Tuple


class Solution:
    def longestPalindrome(self, input_string: str) -> str:
        """
        Find the longest palindromic substring in the given string.
        
        Args:
            input_string: The input string to search for palindromes
            
        Returns:
            The longest palindromic substring found
            
        Raises:
            ValueError: If input string is None
        """
        if input_string is None:
            raise ValueError("Input string cannot be None")
        
        if len(input_string) <= 1:
            return input_string
        
        longest_palindrome_start = 0
        longest_palindrome_length = 1
        
        for center_index in range(len(input_string)):
            # Check for odd-length palindromes centered at center_index
            odd_length_start, odd_length = self._expand_around_center(
                input_string, center_index, center_index
            )
            
            # Check for even-length palindromes centered between center_index and center_index + 1
            even_length_start, even_length = self._expand_around_center(
                input_string, center_index, center_index + 1
            )
            
            # Update longest palindrome if we found a longer one
            if odd_length > longest_palindrome_length:
                longest_palindrome_start = odd_length_start
                longest_palindrome_length = odd_length
                
            if even_length > longest_palindrome_length:
                longest_palindrome_start = even_length_start
                longest_palindrome_length = even_length
        
        return input_string[longest_palindrome_start:longest_palindrome_start + longest_palindrome_length]
    
    def _expand_around_center(self, input_string: str, left_index: int, right_index: int) -> Tuple[int, int]:
        """
        Expand around the given center indices to find the longest palindrome.
        
        Args:
            input_string: The string to search in
            left_index: Left center index
            right_index: Right center index
            
        Returns:
            Tuple of (start_index, length) of the palindrome found
        """
        # Expand while characters match and indices are valid
        while (left_index >= 0 and 
               right_index < len(input_string) and 
               input_string[left_index] == input_string[right_index]):
            left_index -= 1
            right_index += 1
        
        # Adjust indices back to last valid palindrome boundaries
        palindrome_start = left_index + 1
        palindrome_length = right_index - left_index - 1
        
        return palindrome_start, palindrome_length