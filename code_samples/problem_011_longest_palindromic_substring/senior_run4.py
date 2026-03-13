class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Find the longest palindromic substring in the given string.
        
        Uses expand around centers approach to check for palindromes.
        Time complexity: O(n^2), Space complexity: O(1).
        
        Args:
            s: Input string to search for palindromes
            
        Returns:
            The longest palindromic substring found
        """
        if not s:
            return ""
        
        longest_palindrome_start: int = 0
        max_palindrome_length: int = 1
        
        for center_index in range(len(s)):
            # Check for odd-length palindromes centered at current index
            odd_length_palindrome = self._expand_around_center(s, center_index, center_index)
            
            # Check for even-length palindromes centered between current and next index
            even_length_palindrome = self._expand_around_center(s, center_index, center_index + 1)
            
            # Find the longer palindrome between odd and even length
            current_max_length = max(len(odd_length_palindrome), len(even_length_palindrome))
            
            # Update global maximum if current palindrome is longer
            if current_max_length > max_palindrome_length:
                max_palindrome_length = current_max_length
                if len(odd_length_palindrome) > len(even_length_palindrome):
                    longest_palindrome_start = center_index - len(odd_length_palindrome) // 2
                else:
                    longest_palindrome_start = center_index - len(even_length_palindrome) // 2 + 1
        
        return s[longest_palindrome_start:longest_palindrome_start + max_palindrome_length]
    
    def _expand_around_center(self, string: str, left_pointer: int, right_pointer: int) -> str:
        """
        Expand around the given center indices to find the longest palindrome.
        
        Args:
            string: The input string to search within
            left_pointer: Left center index
            right_pointer: Right center index
            
        Returns:
            The palindromic substring found by expanding around the center
        """
        # Expand outward while characters match and indices are valid
        while (left_pointer >= 0 and 
               right_pointer < len(string) and 
               string[left_pointer] == string[right_pointer]):
            left_pointer -= 1
            right_pointer += 1
        
        # Return the palindrome found (adjust indices since loop went one step too far)
        return string[left_pointer + 1:right_pointer]