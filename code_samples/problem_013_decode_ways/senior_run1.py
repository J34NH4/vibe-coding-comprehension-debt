from typing import Dict

class Solution:
    def numDecodings(self, s: str) -> int:
        """
        Calculate the number of ways to decode a string of digits.
        
        Args:
            s: String containing only digits
            
        Returns:
            Number of possible decodings
            
        Raises:
            ValueError: If string contains invalid characters
        """
        if not s or s[0] == '0':
            return 0
            
        # Validate input contains only digits
        if not s.isdigit():
            raise ValueError("Input string must contain only digits")
            
        memo_cache: Dict[int, int] = {}
        return self._decode_with_memoization(s, 0, memo_cache)
    
    def _decode_with_memoization(self, digit_string: str, current_index: int, memo_cache: Dict[int, int]) -> int:
        """
        Helper function to calculate decodings using memoization.
        
        Args:
            digit_string: The input string of digits
            current_index: Current position in the string
            memo_cache: Dictionary to store computed results
            
        Returns:
            Number of ways to decode from current position
        """
        # Base case: reached end of string
        if current_index == len(digit_string):
            return 1
            
        # Check memoization cache
        if current_index in memo_cache:
            return memo_cache[current_index]
            
        # Cannot decode if current digit is '0'
        if digit_string[current_index] == '0':
            memo_cache[current_index] = 0
            return 0
            
        total_ways = 0
        
        # Try single digit decoding (1-9)
        total_ways += self._decode_with_memoization(digit_string, current_index + 1, memo_cache)
        
        # Try two digit decoding (10-26) if possible
        if self._is_valid_two_digit_code(digit_string, current_index):
            total_ways += self._decode_with_memoization(digit_string, current_index + 2, memo_cache)
        
        memo_cache[current_index] = total_ways
        return total_ways
    
    def _is_valid_two_digit_code(self, digit_string: str, start_index: int) -> bool:
        """
        Check if two digits starting at given index form a valid code (10-26).
        
        Args:
            digit_string: The input string of digits
            start_index: Starting index to check two digits
            
        Returns:
            True if the two digits form a valid code, False otherwise
        """
        # Need at least two digits remaining
        if start_index + 1 >= len(digit_string):
            return False
            
        two_digit_number = int(digit_string[start_index:start_index + 2])
        return 10 <= two_digit_number <= 26