class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Find the longest palindromic substring in the given string.
        
        Args:
            s: Input string to search for palindromes
            
        Returns:
            The longest palindromic substring found
            
        Raises:
            ValueError: If input string is None
        """
        if s is None:
            raise ValueError("Input string cannot be None")
        
        if len(s) <= 1:
            return s
        
        longest_palindrome = ""
        
        for center_index in range(len(s)):
            # Check for odd-length palindromes centered at current index
            odd_palindrome = self._expand_around_center(s, center_index, center_index)
            
            # Check for even-length palindromes centered between current and next index
            even_palindrome = self._expand_around_center(s, center_index, center_index + 1)
            
            # Update longest palindrome if we found a longer one
            current_longest = odd_palindrome if len(odd_palindrome) > len(even_palindrome) else even_palindrome
            
            if len(current_longest) > len(longest_palindrome):
                longest_palindrome = current_longest
        
        return longest_palindrome
    
    def _expand_around_center(self, input_string: str, left_pointer: int, right_pointer: int) -> str:
        """
        Expand around the given center indices to find the longest palindrome.
        
        Args:
            input_string: The string to search within
            left_pointer: Left center index
            right_pointer: Right center index
            
        Returns:
            The palindromic substring found by expanding around the center
        """
        # Expand outward while characters match and indices are valid
        while (left_pointer >= 0 and 
               right_pointer < len(input_string) and 
               input_string[left_pointer] == input_string[right_pointer]):
            left_pointer -= 1
            right_pointer += 1
        
        # Return the palindrome (adjust indices since we went one step too far)
        return input_string[left_pointer + 1:right_pointer]